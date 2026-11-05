# ⚡ Cheat Sheet: Laravel API untuk Aplikasi Mobile

[← Dokumen Pendukung](README.md) · Rinci: [Struktur Laravel API](../arsitektur/02-struktur-laravel-api.md)

---

## 1. Artisan yang Sering Dipakai

| Perintah | Fungsi |
|---|---|
| `php artisan install:api` | Pasang Sanctum + `routes/api.php` |
| `php artisan install:broadcasting` | Pasang Reverb + konfigurasi broadcasting |
| `php artisan make:model Attendance -mfs` | Model + migration + factory + seeder |
| `php artisan make:controller Api/V1/CheckInController --invokable` | Controller satu aksi |
| `php artisan make:request Api/V1/CheckInRequest` | Form Request |
| `php artisan make:resource V1/AttendanceResource` | API Resource |
| `php artisan make:policy AttendancePolicy --model=Attendance` | Policy |
| `php artisan make:job GenerateAttendanceThumbnail` | Job queue |
| `php artisan make:event LeaveRequestStatusChanged` | Event |
| `php artisan make:enum AttendanceStatus` | Enum |
| `php artisan make:test Api/V1/CheckInTest --pest` | Test Pest |
| `php artisan route:list --path=api` | Lihat semua route API |
| `php artisan migrate:fresh --seed` | Reset DB + seed |
| `php artisan queue:work` | Jalankan worker |
| `php artisan reverb:start` | Jalankan server WebSocket |
| `php artisan schedule:work` | Jalankan scheduler (lokal) |
| `php artisan tinker` | REPL untuk mencoba kode |

## 2. Pola Satu Endpoint

```php
// routes/api.php
Route::prefix('v1')->middleware(['auth:sanctum', 'throttle:api'])->group(function () {
    Route::post('attendances/check-in', CheckInController::class);
});

// Controller tipis
public function __invoke(CheckInRequest $request, CheckInAction $action): AttendanceResource
{
    return AttendanceResource::make($action->execute($request->user(), $request->validated()));
}
```

## 3. Sanctum (Token untuk Mobile)

```php
$token = $user->createToken($request->device_name, ['*'], now()->addDays(30))->plainTextToken;
$request->user()->currentAccessToken()->delete();   // logout device ini
$user->tokens()->delete();                          // logout semua device
Sanctum::actingAs($user);                           // di test
```

## 4. Validasi

```php
public function rules(): array
{
    return [
        'latitude'   => ['required', 'numeric', 'between:-90,90'],
        'photo'      => ['required', 'image', 'max:2048'],
        'type'       => ['required', Rule::enum(LeaveType::class)],
        'end_date'   => ['required', 'date', 'after_or_equal:start_date'],
        'attachment' => ['nullable', 'required_if:type,sick', 'file', 'mimes:jpg,png,pdf'],
    ];
}
```

## 5. Resource & Pagination

```php
return AttendanceResource::make($attendance);                                  // { data: {...} }
return AttendanceResource::collection($query->cursorPaginate(20));             // { data, links, meta }

// Di Resource
'check_in_at' => $this->check_in_at?->toIso8601String(),
'office'      => OfficeResource::make($this->whenLoaded('office')),
'is_late'     => $this->when($request->user()->isAdmin(), $this->is_late),
```

## 6. Error Bisnis dengan Kode

```php
throw new BusinessException('Anda berada di luar area kantor.', 'OUTSIDE_GEOFENCE',
    meta: ['distance_meters' => 340]);
// → 422 { "message": "...", "code": "OUTSIDE_GEOFENCE", "meta": {...} }
```

## 7. Policy (Cegah IDOR)

```php
public function view(User $user, Attendance $attendance): bool
{
    return $user->id === $attendance->user_id || $user->role === 'admin';
}
// Controller: Gate::authorize('view', $attendance);
```

## 8. Queue, Event, Broadcast

```php
GenerateAttendanceThumbnail::dispatch($attendance)->afterCommit();

class LeaveRequestStatusChanged implements ShouldBroadcast
{
    public function broadcastOn(): array { return [new PrivateChannel("user.{$this->leave->user_id}")]; }
    public function broadcastAs(): string { return 'leave-request.status-changed'; }
}

// routes/channels.php
Broadcast::channel('user.{id}', fn ($user, $id) => (int) $user->id === (int) $id);
```

## 9. Scheduler (`routes/console.php`)

```php
Schedule::command('attendance:remind-check-in')->weekdays()->at('07:45');
Schedule::command('attendance:mark-absent')->dailyAt('23:30');
Schedule::command('sanctum:prune-expired --hours=24')->daily();
```

## 10. Test Pest

```php
it('menolak check-in di luar radius', function () {
    Sanctum::actingAs(User::factory()->create());
    $this->postJson('/api/v1/attendances/check-in', [...])
        ->assertUnprocessable()
        ->assertJsonPath('code', 'OUTSIDE_GEOFENCE');
});
```

| Fake | Untuk |
|---|---|
| `Storage::fake('public')` | Upload file |
| `Queue::fake()` | Pastikan job di-dispatch |
| `Notification::fake()` | Pastikan notifikasi dikirim |
| `Event::fake()` | Pastikan event dipicu |
| `Http::fake()` | Mock API eksternal (Expo Push) |
| `$this->travelTo(...)` | Atur waktu (uji terlambat / tepat waktu) |
