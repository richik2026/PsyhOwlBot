import OwlCore from "../components/OwlCore";
import BottomNav from "../components/BottomNav";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#09060f] text-white overflow-hidden flex flex-col items-center p-6">
      <header className="w-full flex justify-between items-center pt-4">
        <div>
          <h1 className="text-4xl font-serif">Совёнок ♡</h1>
          <p className="text-xs tracking-[0.25em] text-purple-200 mt-2">ТВОЙ AI-ПСИХОЛОГ</p>
        </div>
        <button className="rounded-full bg-white/5 border border-purple-300/20 p-3">⚙</button>
      </header>

      <p className="mt-8 text-purple-200 text-center">Голосовые разговоры, которые помогают</p>

      <section className="flex-1 flex flex-col justify-center items-center gap-8">
        <OwlCore state="idle" />

        <div className="rounded-3xl border border-purple-400/20 bg-white/5 backdrop-blur-xl px-6 py-3 text-center">
          <p>Я рядом. Давай поговорим</p>
        </div>

        <button className="w-full max-w-sm rounded-3xl bg-purple-600 px-10 py-5 text-xl shadow-[0_0_50px_rgba(168,85,247,.45)]">
          🎙 Начать разговор
        </button>
      </section>

      <BottomNav />
    </main>
  );
}
