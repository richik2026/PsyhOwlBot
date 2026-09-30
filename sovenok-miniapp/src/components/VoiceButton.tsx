import { Mic } from 'lucide-react';

export default function VoiceButton({onStart}:{onStart:()=>void}){
 return <button onClick={onStart} className="w-24 h-24 rounded-full bg-purple-600 shadow-[0_0_70px_#9333ea] flex items-center justify-center">
  <Mic size={42}/>
 </button>
}