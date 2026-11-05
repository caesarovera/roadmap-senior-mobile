# ⚡ Cheat Sheet: JavaScript & TypeScript

[← Dokumen Pendukung](README.md) · Latihan: [js-ts-playground](https://github.com/caesarovera/js-ts-playground)

---

## 1. Variabel & Scope

```js
const a = 1;      // tidak bisa di-assign ulang (isi object/array tetap bisa diubah)
let b = 2;        // block scope, bisa di-assign ulang
var c = 3;        // function scope + hoisting. HINDARI.
```

| | `var` | `let` | `const` |
|---|---|---|---|
| Scope | fungsi | blok `{}` | blok `{}` |
| Assign ulang | ✅ | ✅ | ❌ |
| Dipakai sebelum dideklarasi | `undefined` | ❌ error (TDZ) | ❌ error (TDZ) |

## 2. Data Modern

```js
const { nama, kantor: { kota } = {} } = user;      // destructuring + default
const [pertama, ...sisa] = list;                    // rest
const baru = { ...lama, nama: 'Rina' };             // spread (salinan dangkal)
const kota = user?.kantor?.kota ?? 'Tidak ada';     // optional chaining + nullish
```

| Method | Kembali | Mutasi? |
|---|---|---|
| `map`, `filter`, `slice`, `concat` | array baru | ❌ |
| `toSorted`, `toReversed`, `toSpliced`, `with` | array baru | ❌ |
| `sort`, `reverse`, `splice`, `push`, `pop` | — | ⚠️ **ya**, jangan dipakai pada state |
| `reduce` | nilai apa pun | ❌ |
| `find` / `findIndex` / `some` / `every` | item / index / boolean | ❌ |

```js
// Immutable update yang sering dipakai
const tambah = [...list, item];
const ubah   = list.map(x => x.id === id ? { ...x, selesai: true } : x);
const hapus  = list.filter(x => x.id !== id);
```

## 3. `this`

| Pemanggilan | `this` |
|---|---|
| `obj.method()` | `obj` |
| `const f = obj.method; f()` | `undefined` (strict mode) |
| `f.call(x, a, b)` / `f.apply(x, [a, b])` / `f.bind(x)` | `x` |
| `new F()` | object baru |
| Arrow function | `this` dari tempat arrow function itu ditulis |

## 4. Async

```js
// Urutan: sinkron → SEMUA microtask → SATU macrotask → ulangi
try {
  const res = await fetch(url, { signal: AbortSignal.timeout(10_000) });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = await res.json();
} catch (e) { /* jaringan, timeout, atau HTTP error */ }
```

| Fungsi | Kapan dipakai |
|---|---|
| `Promise.all([...])` | Semua harus berhasil; gagal satu = gagal semua |
| `Promise.allSettled([...])` | Ingin tahu hasil masing-masing, tidak peduli ada yang gagal |
| `Promise.race([...])` | Ambil yang selesai **pertama** (sukses atau gagal) |
| `Promise.any([...])` | Ambil yang **berhasil** pertama |

⚠️ `await` di dalam `forEach` **tidak** menunggu. Pakai `for...of` (berurutan) atau `Promise.all(list.map(...))` (paralel).

## 5. TypeScript: Dasar

```ts
type Status = 'tepat_waktu' | 'terlambat';           // union literal
type Koordinat = [lat: number, lng: number];          // tuple
interface Karyawan { readonly id: number; nama: string; jabatan?: string }

function f(x: unknown) {                              // unknown, BUKAN any
  if (typeof x === 'string') x.toUpperCase();         // narrowing
  if (typeof x === 'object' && x !== null && 'message' in x) { /* ... */ }
}

function isApiError(x: unknown): x is ApiError { /* ... */ }   // type guard

const config = { mode: 'prod' } as const;             // literal readonly
const user = { id: 1 } satisfies Partial<Karyawan>;   // cek tipe tanpa mengubah inferensi
```

## 6. TypeScript: Lanjutan

| Utility | Hasil |
|---|---|
| `Partial<T>` / `Required<T>` | Semua field opsional / wajib |
| `Pick<T, 'a' \| 'b'>` / `Omit<T, 'a'>` | Ambil / buang field |
| `Record<K, V>` | Object dengan key K dan nilai V |
| `ReturnType<typeof fn>` | Tipe hasil fungsi |
| `Awaited<Promise<T>>` | `T` |
| `Parameters<typeof fn>` | Tuple tipe parameter |
| `NonNullable<T>` | Buang `null` dan `undefined` |

```ts
// Generic + constraint
function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> { /* ... */ }

// Discriminated union + exhaustive check
type State<T> = { status: 'loading' } | { status: 'success'; data: T } | { status: 'error'; error: string };
switch (s.status) {
  case 'loading': ...; case 'success': ...; case 'error': ...;
  default: { const _never: never = s; }
}

// Mapped, conditional, infer, template literal
type Ro<T> = { readonly [K in keyof T]: T[K] };
type Unwrap<T> = T extends Promise<infer U> ? U : T;
type Camel<S extends string> = S extends `${infer H}_${infer T}` ? `${H}${Capitalize<Camel<T>>}` : S;
```

## 7. Zod

```ts
import { z } from 'zod';

const User = z.object({
  id: z.number().int(),
  email: z.email(),
  role: z.enum(['employee', 'admin']),
  avatar_url: z.url().nullable(),
});
type User = z.infer<typeof User>;            // tipe TS dari schema

const r = User.safeParse(data);              // tidak melempar error
if (!r.success) console.log(r.error.issues);
```

## 8. `tsconfig` Minimal untuk Proyek Serius

```json
{ "compilerOptions": { "strict": true, "noUncheckedIndexedAccess": true } }
```
