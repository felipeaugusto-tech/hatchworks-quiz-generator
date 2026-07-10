"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { fetchQuizzes, generateQuiz, uploadFile, type QuizListItem } from "@/lib/api";

const ACCEPTED_TYPES = ".mp4,.mp3,.wav,.m4a";
const PROGRESS_STEPS = [
  "Uploading...",
  "Transcribing audio...",
  "Generating questions...",
  "Redirecting to quiz...",
] as const;

export function UploadForm() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [numQuestions, setNumQuestions] = useState(5);
  const [progressIndex, setProgressIndex] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [recentQuizzes, setRecentQuizzes] = useState<QuizListItem[]>([]);

  useEffect(() => {
    fetchQuizzes().then(setRecentQuizzes).catch(() => setRecentQuizzes([]));
  }, []);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!file) {
      setError("Choose an audio or video file first.");
      return;
    }

    setError(null);

    try {
      setProgressIndex(0);
      const transcription = await uploadFile(file);

      setProgressIndex(1);
      await new Promise((resolve) => setTimeout(resolve, 250));

      setProgressIndex(2);
      const quiz = await generateQuiz({
        transcription_id: transcription.transcription_id,
        num_questions: numQuestions,
      });

      setProgressIndex(3);
      router.push(`/quiz/${quiz.id}`);
    } catch (submissionError) {
      const message = submissionError instanceof Error ? submissionError.message : "Unexpected error.";
      setError(message);
      setProgressIndex(null);
    }
  }

  return (
    <div className="mx-auto flex min-h-screen max-w-5xl flex-col gap-8 px-6 py-12">
      <section className="rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl shadow-black/30">
        <p className="mb-3 text-sm uppercase tracking-[0.3em] text-blue-300">Upload to Quiz</p>
        <h1 className="text-4xl font-semibold tracking-tight">HatchWorks Quiz Generator</h1>
        <p className="mt-3 max-w-2xl text-white/70">
          Upload a lesson recording, transcribe it with Whisper, and generate an interactive quiz from the result.
        </p>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <label className="block rounded-2xl border border-dashed border-white/20 bg-black/20 p-6">
            <span className="mb-3 block text-sm text-white/70">Audio or video file</span>
            <input
              className="block w-full text-sm text-white file:mr-4 file:rounded-xl file:border-0 file:bg-selected file:px-4 file:py-2 file:text-sm file:font-medium"
              type="file"
              accept={ACCEPTED_TYPES}
              onChange={(event) => setFile(event.target.files?.[0] ?? null)}
            />
          </label>

          <label className="block max-w-xs">
            <span className="mb-3 block text-sm text-white/70">Number of questions</span>
            <input
              className="w-full rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-white outline-none ring-0"
              type="number"
              min={3}
              max={15}
              value={numQuestions}
              onChange={(event) => setNumQuestions(Number(event.target.value))}
            />
          </label>

          <button
            className="rounded-xl bg-selected px-6 py-3 font-medium text-white transition hover:bg-blue-500"
            type="submit"
            disabled={!file || progressIndex !== null}
          >
            Generate Quiz
          </button>
        </form>

        {progressIndex !== null ? (
          <ol className="mt-8 space-y-2 rounded-2xl border border-white/10 bg-black/20 p-5 text-sm text-white/80">
            {PROGRESS_STEPS.map((step, index) => (
              <li key={step} className={index <= progressIndex ? "text-white" : "text-white/40"}>
                {index < progressIndex ? "✅" : "⏳"} {step}
              </li>
            ))}
          </ol>
        ) : null}

        {error ? (
          <div className="mt-6 rounded-xl border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-200">{error}</div>
        ) : null}
      </section>

      <section className="rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl shadow-black/30">
        <h2 className="text-xl font-semibold">Recent quizzes</h2>
        {recentQuizzes.length === 0 ? (
          <p className="mt-4 text-white/60">No quizzes yet.</p>
        ) : (
          <ul className="mt-4 space-y-3">
            {recentQuizzes.map((quiz) => (
              <li key={quiz.id} className="rounded-2xl border border-white/10 bg-black/20 p-4">
                <button className="text-left" onClick={() => router.push(`/quiz/${quiz.id}`)} type="button">
                  <div className="font-medium text-white">{quiz.title}</div>
                  <div className="mt-1 text-sm text-white/60">
                    {quiz.num_questions} questions · {new Date(quiz.created_at).toLocaleString()}
                  </div>
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}