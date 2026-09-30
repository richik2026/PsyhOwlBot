import OwlCore from "../components/OwlCore";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#09060f] text-white flex flex-col items-center justify-center gap-8 p-6">
      <h1 className="text-4xl font-serif">Совёнок</h1>
      <p className="text-purple-200">Я рядом. Давай поговорим</p>

      <OwlCore state="idle" />

      <button className="rounded-2xl bg-purple-600 px-10 py-5 text-xl shadow-[0_0_40px_rgba(168,85,247,.5)]">
        🎙 Начать разговор
      </button>
    </main>
  );
}
