"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams, useRouter } from "next/navigation";

import { QuestionCard } from "@/components/QuestionCard";
import { fetchQuiz, type Quiz } from "@/lib/api";

const STORAGE_KEY_PREFIX = "quiz-answers:";

export default function QuizPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const quizId = params.id;
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, "A" | "B" | "C" | "D">>({});
  const [showAnswer, setShowAnswer] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchQuiz(quizId)
      .then((payload) => {
        setQuiz(payload);
        const cached = window.localStorage.getItem(`${STORAGE_KEY_PREFIX}${payload.id}`);
        if (cached) {
          setAnswers(JSON.parse(cached));
        }
      })
      .catch((fetchError) => setError(fetchError instanceof Error ? fetchError.message : "Failed to load quiz."));
  }, [quizId]);

  const question = useMemo(() => quiz?.questions[currentIndex] ?? null, [quiz, currentIndex]);

  if (error) {
    return <main className="mx-auto max-w-4xl p-10 text-red-300">{error}</main>;
  }

  if (!quiz || !question) {
    return <main className="mx-auto max-w-4xl p-10 text-white/70">Loading quiz...</main>;
  }

  function handleSelect(option: "A" | "B" | "C" | "D") {
    const next = { ...answers, [question.position]: option };
    setAnswers(next);
    window.localStorage.setItem(`${STORAGE_KEY_PREFIX}${quiz.id}`, JSON.stringify(next));
    setShowAnswer(true);
  }

  function handleNext() {
    if (currentIndex === quiz.questions.length - 1) {
      router.push(`/results/${quiz.id}`);
      return;
    }
    setCurrentIndex((value) => value + 1);
    setShowAnswer(false);
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-4xl flex-col gap-6 px-6 py-12">
      <div className="rounded-2xl border border-white/10 bg-black/20 px-5 py-4 text-white/70">
        Question {currentIndex + 1} of {quiz.questions.length}
      </div>

      <QuestionCard
        question={question}
        selectedOption={answers[question.position] ?? null}
        showAnswer={showAnswer}
        onSelect={handleSelect}
      />

      {showAnswer ? (
        <button
          type="button"
          className="self-end rounded-xl bg-selected px-6 py-3 font-medium text-white hover:bg-blue-500"
          onClick={handleNext}
        >
          {currentIndex === quiz.questions.length - 1 ? "See Results" : "Next Question"}
        </button>
      ) : null}
    </main>
  );
}