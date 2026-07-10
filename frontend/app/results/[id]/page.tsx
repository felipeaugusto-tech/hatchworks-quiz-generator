"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams, useRouter } from "next/navigation";

import { ResultsSummary, type SavedAnswers } from "@/components/ResultsSummary";
import { fetchQuiz, type Quiz } from "@/lib/api";

const STORAGE_KEY_PREFIX = "quiz-answers:";

export default function ResultsPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const quizId = params.id;
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [answers, setAnswers] = useState<SavedAnswers>({});
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchQuiz(quizId)
      .then((payload) => {
        setQuiz(payload);
        const cached = window.localStorage.getItem(`${STORAGE_KEY_PREFIX}${payload.id}`);
        if (cached) {
          setAnswers(JSON.parse(cached) as SavedAnswers);
        }
      })
      .catch((fetchError) => setError(fetchError instanceof Error ? fetchError.message : "Failed to load results."));
  }, [quizId]);

  const score = useMemo(() => {
    if (!quiz) {
      return 0;
    }
    return quiz.questions.reduce((total, question) => {
      return total + (answers[question.position] === question.correct ? 1 : 0);
    }, 0);
  }, [answers, quiz]);

  if (error) {
    return <main className="mx-auto max-w-4xl p-10 text-red-300">{error}</main>;
  }

  if (!quiz) {
    return <main className="mx-auto max-w-4xl p-10 text-white/70">Loading results...</main>;
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-4xl flex-col gap-6 px-6 py-12">
      <ResultsSummary quiz={quiz} answers={answers} score={score} />
      <button
        type="button"
        className="self-end rounded-xl bg-selected px-6 py-3 font-medium text-white hover:bg-blue-500"
        onClick={() => router.push("/")}
      >
        Generate Another Quiz
      </button>
    </main>
  );
}