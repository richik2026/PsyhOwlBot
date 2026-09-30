import { motion } from 'framer-motion';

export default function OwlVoiceOrb({state='listening'}:{state?:string}) {
  const speaking = state === 'speaking';
  const thinking = state === 'thinking';

  return (
    <div className="relative flex items-center justify-center h-96">
      <motion.div
        animate={{scale: speaking ? [1,1.45,1] : thinking ? [1,1.2,1] : [1,1.1,1]}}
        transition={{duration:1.8,repeat:Infinity}}
        className="absolute w-80 h-80 rounded-full border border-purple-400/40"
      />
      <motion.div
        animate={{rotate:360}}
        transition={{duration:12,repeat:Infinity,ease:'linear'}}
        className="absolute w-64 h-64 rounded-full border border-purple-500/30"
      />
      <motion.div
        animate={{boxShadow:['0 0 50px #9333ea','0 0 140px #c084fc','0 0 50px #9333ea']}}
        transition={{duration:2,repeat:Infinity}}
        className="w-44 h-44 rounded-full bg-gradient-to-br from-purple-500 to-violet-900 flex items-center justify-center text-7xl"
      >
        🦉
      </motion.div>
    </div>
  );
}
