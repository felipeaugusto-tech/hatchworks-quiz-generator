import type { Question } from "@/lib/api";

type Props = {
  question: Question;
  selectedOption: "A" | "B" | "C" | "D" | null;
  showAnswer: boolean;
  onSelect: (value: "A" | "B" | "C" | "D") => void;
};

const OPTIONS: Array<{ key: "A" | "B" | "C" | "D"; label: keyof Question }> = [
  { key: "A", label: "option_a" },
  { key: "B", label: "option_b" },
  { key: "C", label: "option_c" },
  { key: "D", label: "option_d" },
];

export function QuestionCard({ question, selectedOption, showAnswer, onSelect }: Props) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl shadow-black/30">
      <p className="text-sm uppercase tracking-[0.3em] text-blue-300">Question {question.position}</p>
      <h2 className="mt-4 text-3xl font-semibold leading-tight">{question.question}</h2>
      <div className="mt-8 grid gap-4">
        {OPTIONS.map((option) => {
          const isSelected = selectedOption === option.key;
          const isCorrect = question.correct === option.key;
          let className = "border-white/10 bg-black/20 hover:border-selected/50 hover:bg-selected/10";

          if (showAnswer && isCorrect) {
            className = "border-correct/60 bg-correct/20";
          } else if (showAnswer && isSelected && !isCorrect) {
            className = "border-wrong/60 bg-wrong/20";
          } else if (isSelected) {
            className = "border-selected/60 bg-selected/20";
          }

          return (
            <button
              key={option.key}
              type="button"
              onClick={() => onSelect(option.key)}
              disabled={showAnswer}
              className={`rounded-2xl border p-5 text-left transition ${className}`}
            >
              <div className="text-sm font-medium text-white/60">{option.key}</div>
              <div className="mt-2 text-lg text-white">{question[option.label]}</div>
            </button>
          );
        })}
      </div>

      {showAnswer ? (
        <div className="mt-6 rounded-2xl border border-white/10 bg-black/20 p-5 text-white/80">
          <p className="font-medium text-white">Explanation</p>
          <p className="mt-2">{question.explanation}</p>
        </div>
      ) : null}
    </div>
  );
}