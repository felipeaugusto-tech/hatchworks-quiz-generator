import type { Quiz } from "@/lib/api";

export type SavedAnswers = Record<number, "A" | "B" | "C" | "D">;

type Props = {
  quiz: Quiz;
  answers: SavedAnswers;
  score: number;
};

const OPTION_LABELS = {
  A: "option_a",
  B: "option_b",
  C: "option_c",
  D: "option_d",
} as const;

export function ResultsSummary({ quiz, answers, score }: Props) {
  const percentage = quiz.questions.length === 0 ? 0 : Math.round((score / quiz.questions.length) * 100);

  return (
    <div className="space-y-6">
      <section className="rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl shadow-black/30">
        <p className="text-sm uppercase tracking-[0.3em] text-blue-300">Results</p>
        <h1 className="mt-3 text-4xl font-semibold">You got {score} out of {quiz.questions.length} correct!</h1>
        <p className="mt-3 text-xl text-white/70">{percentage}% overall score</p>
      </section>

      <section className="space-y-4">
        {quiz.questions.map((question) => {
          const answer = answers[question.position];
          const correct = question.correct === answer;
          const correctLabel = OPTION_LABELS[question.correct];
          const answerLabel = answer ? OPTION_LABELS[answer] : null;

          return (
            <article key={question.id} className="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-2xl shadow-black/30">
              <div className="text-sm text-white/60">{correct ? "✅ Correct" : "❌ Incorrect"}</div>
              <h2 className="mt-2 text-xl font-semibold">{question.question}</h2>
              <p className="mt-4 text-white/70">Your answer: {answer ? question[answerLabel!] : "No answer recorded"}</p>
              <p className="mt-2 text-white/70">Correct answer: {question[correctLabel]}</p>
              <p className="mt-4 rounded-2xl border border-white/10 bg-black/20 p-4 text-white/80">{question.explanation}</p>
            </article>
          );
        })}
      </section>
    </div>
  );
}