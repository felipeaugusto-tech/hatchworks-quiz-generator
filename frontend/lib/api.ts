export type TranscribeResponse = {
  transcription_id: string;
  duration_s: number;
  preview: string;
};

export type GenerateQuizRequest = {
  transcription_id: string;
  num_questions: number;
};

export type Question = {
  id: string;
  position: number;
  question: string;
  option_a: string;
  option_b: string;
  option_c: string;
  option_d: string;
  correct: "A" | "B" | "C" | "D";
  explanation: string;
};

export type Quiz = {
  id: string;
  transcription_id: string;
  title: string;
  num_questions: number;
  created_at: string;
  questions: Question[];
};

export type QuizListItem = {
  id: string;
  title: string;
  num_questions: number;
  created_at: string;
};

export type TranscriptionListItem = {
  id: string;
  filename: string;
  duration_s: number | null;
  created_at: string;
  preview: string;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function fetchQuizzes(): Promise<QuizListItem[]> {
  return request<QuizListItem[]>("/quizzes");
}

export async function fetchQuiz(id: string): Promise<Quiz> {
  return request<Quiz>(`/quiz/${id}`);
}

export async function uploadFile(file: File): Promise<TranscribeResponse> {
  const formData = new FormData();
  formData.append("file", file);
  return request<TranscribeResponse>("/transcribe", { method: "POST", body: formData });
}

export async function generateQuiz(payload: GenerateQuizRequest): Promise<Quiz> {
  return request<Quiz>("/quiz/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}