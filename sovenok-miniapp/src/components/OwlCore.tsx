import { motion } from 'framer-motion';

export default function OwlCore({state='idle'}:{state?:string}) {
 const speaking = state === 'speaking';
 return <div className="relative flex items-center justify-center">
  <motion.div animate={{scale:speaking?[1,1.35,1]:[1,1.15,1],opacity:[0.4,0.8,0.4]}} transition={{duration:2,repeat:Infinity}} className="absolute w-72 h-72 rounded-full border border-purple-500/40" />
  <motion.div animate={{boxShadow:['0 0 40px #9333ea','0 0 120px #a855f7','0 0 40px #9333ea']}} transition={{duration:2,repeat:Infinity}} className="w-44 h-44 rounded-full bg-gradient-to-br from-purple-500 to-indigo-700 flex items-center justify-center text-7xl">🦉</motion.div>
 </div>
}