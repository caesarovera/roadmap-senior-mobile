# Fase 0 — JavaScript Mendalam, TypeScript, React

[← Kembali ke README](../README.md) · **Durasi: 8 minggu** · Repo latihan: `js-ts-playground`, `react-web-latihan`

## Kenapa fase ini penting?

Sebagian besar bug dan masalah performa di React Native **bukan** masalah React Native, tapi masalah pemahaman JavaScript dan React. Contohnya closure yang menyimpan nilai basi, re-render tak terkendali, atau Promise yang tidak di-handle. Di level semi-middle, area inilah yang paling sering bolong.

**Hasil akhir fase:** Anda bisa menjelaskan *kenapa* kode JS/React berperilaku tertentu, bukan hanya *bahwa* kode itu bekerja.

---

## Minggu 1 — Fondasi JavaScript: Tipe, Scope, Closure

🎯 **Tujuan:** memahami cara JavaScript menyimpan nilai dan mengelola variabel.

📚 **Materi**
- Tipe primitif vs reference (object, array, function)
- `==` vs `===`, type coercion, nilai *truthy*/*falsy*
- `var` vs `let` vs `const`, block scope, *hoisting*, *temporal dead zone*
- **Closure**: fungsi yang "mengingat" lingkungan tempat ia dibuat
- Sumber: [javascript.info, bagian 1–6](https://javascript.info/) · [You Don't Know JS Yet: Scope & Closures](https://github.com/getify/You-Dont-Know-JS)

🛠 **Latihan**
1. Buat fungsi `createCounter()` yang mengembalikan `{ increment, decrement, getValue }` tanpa variabel global.
2. Buat fungsi `once(fn)`: `fn` hanya boleh dijalankan sekali, panggilan berikutnya mengembalikan hasil pertama.
3. Buat `memoize(fn)` sederhana yang meng-cache hasil berdasarkan argumen.
4. Tebak output kode berikut, lalu jalankan dan jelaskan:
   ```js
   for (var i = 0; i < 3; i++) setTimeout(() => console.log(i), 0);
   for (let j = 0; j < 3; j++) setTimeout(() => console.log(j), 0);
   ```

✅ **Checkpoint**
- Kenapa loop `var` mencetak `3 3 3` sedangkan loop `let` mencetak `0 1 2`?
- Apa yang terjadi saat Anda mengubah properti object yang di-`const`?

---

## Minggu 2 — `this`, Prototype, Class, Module

🎯 **Tujuan:** paham cara kerja object dan sistem modul JavaScript.

📚 **Materi**
- Aturan `this`: default, implicit, explicit (`call`/`apply`/`bind`), `new`, arrow function
- Prototype chain dan hubungannya dengan `class`
- `class`: constructor, method, getter/setter, field privat `#`, `static`, `extends`
- ES Modules: `import`/`export`, named vs default export, dynamic `import()`

🛠 **Latihan**
1. Buat class `EventEmitter` dengan method `on`, `off`, `emit`, `once`.
2. Tulis ulang `EventEmitter` tanpa `class` (pakai function + prototype). Bandingkan.
3. Buat bug `this` dengan sengaja: pakai method class sebagai callback, lalu perbaiki dengan 3 cara berbeda.

✅ **Checkpoint**
- Kenapa arrow function tidak cocok dijadikan method di object literal yang memakai `this`?
- Apa bedanya named export dan default export dari sisi *refactoring* dan *tree-shaking*?

---

## Minggu 3 — Asynchronous JavaScript (sangat penting untuk mobile)

🎯 **Tujuan:** menguasai async karena hampir semua hal di mobile itu async: API, storage, kamera, lokasi.

📚 **Materi**
- **Event loop**: call stack, task queue (macrotask), microtask queue
- Callback → Promise → `async`/`await`
- Error handling: `try/catch`, `.catch()`, *unhandled rejection*
- `Promise.all`, `allSettled`, `race`, `any`, dan kapan memakai masing-masing
- Membatalkan request dengan `AbortController`
- Sumber: [javascript.info: Promises, async/await](https://javascript.info/async) · Video "What the heck is the event loop anyway?" (Philip Roberts)

🛠 **Latihan**
1. Tebak urutan output, lalu jalankan:
   ```js
   console.log('A');
   setTimeout(() => console.log('B'), 0);
   Promise.resolve().then(() => console.log('C'));
   queueMicrotask(() => console.log('D'));
   console.log('E');
   ```
2. Buat fungsi `fetchWithTimeout(url, ms)` memakai `AbortController`.
3. Buat fungsi `retry(fn, { retries, delayMs })` dengan *exponential backoff*.
4. Buat fungsi `runWithConcurrency(tasks, limit)` yang menjalankan maksimal `limit` Promise sekaligus. (Nantinya berguna untuk upload banyak foto.)

✅ **Checkpoint**
- Kenapa `C` dan `D` muncul sebelum `B`?
- Kalau satu dari 5 request di `Promise.all` gagal, apa yang terjadi? Bagaimana kalau pakai `allSettled`?

---

## Minggu 4 — Pola Data Modern & Immutability

🎯 **Tujuan:** terbiasa mengolah data tanpa mutasi. Ini fondasi state management di React.

📚 **Materi**
- `map`, `filter`, `reduce`, `find`, `some`, `every`, `flatMap`
- Destructuring, spread/rest, optional chaining `?.`, nullish coalescing `??`
- **Immutability**: kenapa React butuh referensi baru untuk mendeteksi perubahan
- `structuredClone`, shallow copy vs deep copy
- Method array non-mutasi: `toSorted`, `toReversed`, `with`

🛠 **Latihan**
Diberikan data transaksi (buat sekitar 50 data dummy):
```js
{ id, tanggal, kategori, jenis: 'masuk' | 'keluar', jumlah, catatan }
```
Tulis fungsi murni (pure function) untuk:
1. Total pemasukan dan pengeluaran per bulan
2. Kategori dengan pengeluaran terbesar
3. Mengelompokkan transaksi per tanggal (bentuk data untuk `SectionList` nanti)
4. Mengubah satu transaksi **tanpa memutasi** array aslinya

✅ **Checkpoint**
- Kenapa `state.items.push(x); setState(state)` tidak memicu re-render di React?

---

## Minggu 5 — TypeScript Dasar

🎯 **Tujuan:** menulis kode bertipe dengan nyaman di mode `strict`.

📚 **Materi**
- Setup `tsconfig.json` dengan `"strict": true` (wajib, jangan dimatikan)
- Tipe dasar, array, tuple, `type` vs `interface`
- Union, literal type, `unknown` vs `any` (hindari `any`)
- **Type narrowing**: `typeof`, `in`, `instanceof`, *type guard*
- Optional property, `readonly`, *function type*
- Sumber: [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)

🛠 **Latihan**
1. Migrasikan semua latihan Minggu 1–4 ke TypeScript.
2. Buat tipe `Transaksi` dan pastikan fungsi-fungsi di Minggu 4 bertipe penuh, tanpa `any`.
3. Buat type guard `isApiError(x: unknown): x is ApiError`.

✅ **Checkpoint**
- Kapan memakai `unknown` alih-alih `any`?
- Apa yang diberikan mode `strict` (`strictNullChecks`, `noImplicitAny`, dan lain-lain)?

---

## Minggu 6 — TypeScript Lanjutan

🎯 **Tujuan:** menguasai pola TypeScript yang sering dipakai di kode React Native profesional.

📚 **Materi**
- **Generics**: fungsi, tipe, dan constraint generik (`<T extends ...>`)
- Utility types: `Partial`, `Required`, `Pick`, `Omit`, `Record`, `ReturnType`, `Awaited`
- **Discriminated union**, pola paling penting untuk state UI
- `as const`, `satisfies`, template literal types
- **Zod**: validasi data runtime dan inferensi tipe (`z.infer`). Sumber: [zod.dev](https://zod.dev/)

🛠 **Latihan**
1. Buat tipe state request:
   ```ts
   type RequestState<T> =
     | { status: 'idle' }
     | { status: 'loading' }
     | { status: 'success'; data: T }
     | { status: 'error'; error: string };
   ```
   Lalu buat fungsi `render(state)` yang memakai `switch` dengan *exhaustive check* (`never`).
2. Buat fungsi generik `apiGet<T>(url, schema: z.ZodType<T>): Promise<T>` yang memvalidasi response dengan Zod.
3. Buat tipe response API Laravel Anda sendiri, misalnya `ApiResponse<T>` dan `PaginatedResponse<T>` (lihat [konvensi API](../arsitektur/03-konvensi-api.md)).

✅ **Checkpoint**
- Kenapa data dari API perlu divalidasi saat runtime (Zod) padahal sudah ada tipe TypeScript?

---

## Minggu 7 — React Fundamental (di Web)

🎯 **Tujuan:** memahami **model mental React**. Ini lebih mudah dipelajari di web dulu.

📚 **Materi**
- Setup: `npm create vite@latest` (template `react-ts`)
- Komponen, props, children, komposisi
- `useState`, `useEffect`, dan **siklus render**
- **Kapan komponen re-render**: state berubah, parent re-render, atau context berubah
- `key` pada list dan kenapa index sebagai key berbahaya
- `useEffect` yang benar: dependency array, cleanup, dan kapan **tidak** perlu effect
- Sumber: [react.dev/learn](https://react.dev/learn), terutama [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)

🛠 **Latihan**
1. Aplikasi to-do sederhana: tambah, hapus, tandai selesai, filter.
2. Pasang `console.log('render', namaKomponen)` di setiap komponen dan amati kapan masing-masing render.
3. Buat bug *stale closure* dengan `setInterval` di dalam `useEffect`, lalu perbaiki.

✅ **Checkpoint**
- Jelaskan urutan kejadian dari klik tombol sampai layar berubah.
- Kenapa menyimpan data turunan (misalnya `filteredTodos`) di state adalah anti-pattern?

---

## Minggu 8 — React Lanjutan + Mini Proyek dengan Laravel

🎯 **Tujuan:** menguasai hooks lanjutan dan menghubungkan React ke API Laravel.

📚 **Materi**
- `useReducer` untuk state kompleks
- `useContext` dan masalah re-render-nya
- `useRef` (nilai yang tidak memicu render)
- `React.memo`, `useMemo`, `useCallback`, dan kapan **benar-benar** perlu
- **Custom hooks**: mengekstrak logika yang bisa dipakai ulang
- React DevTools Profiler

🛠 **Latihan: Mini proyek "Katalog Produk"**
- **Backend Laravel:** endpoint `GET /api/v1/products` (pagination, search, filter kategori) dengan API Resource
- **Frontend React (Vite + TS):**
  - Custom hook `useProducts({ search, category, page })`
  - Search dengan **debounce** (buat custom hook `useDebounce`)
  - State loading/error/empty memakai discriminated union dari Minggu 6
  - Batalkan request lama saat user mengetik lagi (`AbortController`)
- Ukur re-render dengan Profiler, lalu optimasi dengan `memo` hanya di tempat yang terbukti perlu

✅ **Checkpoint Fase 0** (wajib lulus sebelum lanjut)
- [ ] Bisa menjelaskan event loop dan urutan microtask/macrotask
- [ ] Bisa menulis TypeScript `strict` tanpa `any`
- [ ] Bisa menjelaskan kapan dan kenapa komponen re-render
- [ ] Bisa membuat custom hook sendiri
- [ ] Paham bahwa `useMemo`/`useCallback` bukan "obat otomatis" untuk performa
- [ ] Mini proyek katalog sudah di GitHub dengan README

---

← [Cara Belajar](00-cara-belajar.md) · Lanjut ke → [Fase 1: Dasar React Native](fase-1-react-native-dasar.md)
