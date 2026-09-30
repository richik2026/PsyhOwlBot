import { motion } from "framer-motion";

type Props = {
  state?: "idle" | "listening" | "speaking";
};

export default function OwlCore({ state = "idle" }: Props) {
  const active = state !== "idle";

  return (
    <div className="relative flex h-72 w-72 items-center justify-center">
      <motion.div
        animate={{
          scale: active ? [1, 1.25, 1] : [1, 1.08, 1],
          opacity: active ? [0.3, 0.8, 0.3] : [0.2, 0.5, 0.2],
        }}
        transition={{ duration: 2, repeat: Infinity }}
        className="absolute h-72 w-72 rounded-full border border-purple-400/40"
      />

      <motion.div
        animate={{
          boxShadow: [
            "0 0 40px rgba(168,85,247,.4)",
            "0 0 120px rgba(168,85,247,.8)",
            "0 0 40px rgba(168,85,247,.4)",
          ],
        }}
        transition={{ duration: 2, repeat: Infinity }}
        className="relative flex h-44 w-44 items-center justify-center rounded-full bg-gradient-to-br from-purple-500 to-indigo-900 text-7xl"
      >
        🦉
      </motion.div>
    </div>
  );
}
