import { motion } from 'framer-motion';
import { Mic } from 'lucide-react';

export default function App(){
 return <div className="min-h-screen bg-[#05020b] text-white flex flex-col items-center justify-center">
  <motion.div animate={{boxShadow:['0 0 40px #9333ea','0 0 120px #a855f7','0 0 40px #9333ea']}} transition={{duration:2,repeat:Infinity}} className="w-44 h-44 rounded-full bg-purple-600 flex items-center justify-center text-7xl">🦉</motion.div>
  <h1 className="text-3xl mt-10">Совёнок</h1>
  <p className="mt-4 text-purple-200 text-center">Я рядом.<br/>Давай поговорим.</p>
  <button className="mt-12 w-56 h-16 rounded-full bg-purple-600 shadow-[0_0_50px_#8b5cf6] flex items-center justify-center gap-3"><Mic/>Начать разговор</button>
 </div>
}