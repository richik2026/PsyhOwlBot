import OwlVoiceOrb from '../components/OwlVoiceOrb';

export default function Voice(){
  return (
    <main className="min-h-screen bg-[#09060f] text-white flex flex-col items-center justify-between p-6">
      <div className="w-full flex justify-between items-center">
        <h1 className="text-xl font-serif">Разговор с Совёнком</h1>
        <button className="rounded-full bg-white/10 px-3 py-2">•••</button>
      </div>

      <section className="flex flex-col items-center gap-6">
        <OwlVoiceOrb state="listening" />
        <h2 className="text-2xl text-purple-100">Слушаю тебя...</h2>
        <div className="text-purple-300">00:24</div>
        <div className="flex gap-10 items-center">
          <button className="rounded-full bg-white/10 p-5">✕</button>
          <button className="rounded-full bg-purple-500 p-7 text-3xl shadow-[0_0_50px_rgba(168,85,247,.7)]">🎙</button>
          <button className="rounded-full bg-white/10 p-5">Ⅱ</button>
        </div>
      </section>

      <div className="w-full rounded-3xl bg-white/5 backdrop-blur p-5 text-center text-purple-100">
        Ты можешь говорить обо всём, что сейчас важно. Я рядом.
      </div>
    </main>
  );
}
