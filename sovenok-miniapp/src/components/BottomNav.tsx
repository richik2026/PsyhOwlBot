export default function BottomNav(){
  return (
    <nav className="fixed bottom-5 left-5 right-5 rounded-3xl border border-purple-400/20 bg-white/5 backdrop-blur-xl px-6 py-4 flex justify-around text-purple-200">
      <button>⌂<span className="block text-xs">Главная</span></button>
      <button>◷<span className="block text-xs">История</span></button>
      <button>✿<span className="block text-xs">Практики</span></button>
      <button>♙<span className="block text-xs">Профиль</span></button>
    </nav>
  );
}
