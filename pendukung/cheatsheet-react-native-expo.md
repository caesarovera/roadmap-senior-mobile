# ⚡ Cheat Sheet: React Native, Expo & State

[← Dokumen Pendukung](README.md)

---

## 1. Perintah Expo & EAS

| Perintah | Fungsi |
|---|---|
| `npx create-expo-app@latest nama` | Proyek baru |
| `npx expo start` | Jalankan dev server (tekan `a` = Android, `i` = iOS, `r` = reload, `j` = debugger) |
| `npx expo start -c` | Jalankan sambil membersihkan cache Metro |
| `npx expo install nama-lib` | Install library dengan versi yang cocok dengan SDK |
| `npx expo install --check` | Cek library yang versinya tidak cocok |
| `npx expo-doctor` | Diagnosa masalah konfigurasi proyek |
| `npx expo run:android` | Build & jalankan development build lokal |
| `npx expo prebuild --clean` | Buat ulang folder `android/` & `ios/` |
| `eas build --profile development --platform android` | Development build di cloud |
| `eas build --profile production --platform android` | Build AAB untuk Play Store |
| `eas submit --platform android` | Kirim build ke Play Console |
| `eas update --channel preview --message "..."` | Kirim OTA update |

## 2. Komponen Inti

| Web | React Native | Catatan |
|---|---|---|
| `<div>` | `<View>` | Default `flexDirection: 'column'` |
| `<span>`, `<p>` | `<Text>` | **Semua teks wajib di dalam `<Text>`** |
| `<img>` | `<Image>` / `expo-image` | `expo-image` punya cache & placeholder |
| `<button>` | `<Pressable>` | Bisa memberi style berbeda saat ditekan |
| `<input>` | `<TextInput>` | `keyboardType`, `secureTextEntry`, `returnKeyType` |
| `overflow: scroll` | `<ScrollView>` | Untuk konten pendek |
| list panjang | `<FlatList>` / `<FlashList>` | **Jangan** `ScrollView` + `.map()` |

## 3. Styling & Layout

```tsx
const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, gap: 12 },
  row: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
});
```

| Kebutuhan | Solusi |
|---|---|
| Notch / status bar | `react-native-safe-area-context` |
| Ukuran layar | `useWindowDimensions()` |
| Beda Android/iOS | `Platform.OS`, `Platform.select({...})`, file `.android.tsx` |
| Keyboard menutupi input | `KeyboardAvoidingView` / `react-native-keyboard-controller` |
| Dark mode | `useColorScheme()` + design tokens |

## 4. Expo Router

```
app/_layout.tsx            → layout root (Stack)
app/(tabs)/_layout.tsx     → bottom tabs
app/(tabs)/index.tsx       → "/"
app/izin/[id].tsx          → "/izin/31"
app/izin/baru.tsx          → "/izin/baru"
app/+not-found.tsx         → 404
```

```tsx
import { Link, router, useLocalSearchParams } from 'expo-router';
<Link href="/izin/31">Detail</Link>
router.push('/izin/baru');      // tambah ke stack
router.replace('/');            // ganti (setelah login / sukses absen)
router.back();
const { id } = useLocalSearchParams<{ id: string }>();
```

## 5. Hooks React

| Hook | Untuk | Jebakan |
|---|---|---|
| `useState` | State lokal | Pakai `setX(prev => ...)` kalau bergantung nilai sebelumnya |
| `useEffect` | Sinkronisasi dengan sistem luar | Wajib cleanup; jangan dipakai untuk fetch (pakai Query) atau data turunan |
| `useMemo` / `useCallback` | Referensi stabil, komputasi berat | Bukan obat otomatis performa; ukur dulu |
| `useRef` | Nilai yang tidak memicu render, akses ke elemen | Jangan dibaca untuk menentukan output render |
| `useReducer` | State kompleks dengan banyak aksi | Reducer harus murni |

## 6. TanStack Query

```tsx
// Ambil data
const { data, isPending, isError, error, refetch, isRefetching } = useQuery({
  queryKey: ['attendance', 'today'],
  queryFn: getToday,
  staleTime: 30_000,
});

// Ubah data
const qc = useQueryClient();
const m = useMutation({
  mutationFn: checkIn,
  onSuccess: (data) => {
    qc.setQueryData(['attendance', 'today'], data);
    qc.invalidateQueries({ queryKey: ['attendance'] });
  },
});
m.mutate(input);  // m.isPending, m.error

// Infinite scroll + cursor Laravel
useInfiniteQuery({
  queryKey: ['attendance', 'history'],
  queryFn: ({ pageParam }) => getHistory(pageParam),
  initialPageParam: null as string | null,
  getNextPageParam: (last) => last.meta.next_cursor,
});
```

| Opsi | Arti |
|---|---|
| `staleTime` | Lama data dianggap segar (default 0 = langsung basi) |
| `gcTime` | Lama cache disimpan setelah tidak dipakai (default 5 menit) |
| `enabled` | `false` = jangan fetch dulu (misalnya belum login) |
| `retry` | Jumlah/aturan retry (jangan retry 4xx) |
| `select` | Transformasi data untuk komponen ini saja |

## 7. Zustand

```ts
const useSettings = create<State>()(persist(
  (set) => ({ tema: 'system', setTema: (tema) => set({ tema }) }),
  { name: 'settings', storage: createJSONStorage(() => mmkvStorage) },
));

const tema = useSettings((s) => s.tema);                          // selector: re-render hanya kalau tema berubah
const { a, b } = useSettings(useShallow((s) => ({ a: s.a, b: s.b })));
useSettings.getState().setTema('dark');                            // di luar komponen
```

## 8. Library Expo yang Sering Dipakai

| Kebutuhan | Library |
|---|---|
| Token / rahasia | `expo-secure-store` |
| Lokasi | `expo-location` |
| Kamera | `expo-camera` |
| Pilih gambar | `expo-image-picker` |
| Kompres gambar | `expo-image-manipulator` |
| Notifikasi | `expo-notifications` |
| Database lokal | `expo-sqlite` |
| File | `expo-file-system` |
| Info device | `expo-device`, `expo-application` |
| Biometrik | `expo-local-authentication` |
| Haptic | `expo-haptics` |
| Splash | `expo-splash-screen` |

## 9. Testing

```tsx
// Jest + React Native Testing Library
render(<LoginScreen />, { wrapper: TestProviders });
await userEvent.type(screen.getByLabelText('Email'), 'a@b.c');
await userEvent.press(screen.getByRole('button', { name: 'Masuk' }));
expect(await screen.findByText('Email atau password salah.')).toBeOnTheScreen();
```

```yaml
# Maestro (.maestro/login.yaml)
appId: com.caesarovera.absensi
---
- launchApp: { clearState: true }
- tapOn: { id: "input-email" }
- inputText: "karyawan@demo.test"
- tapOn: "Masuk"
- assertVisible: "Selamat pagi"
```
