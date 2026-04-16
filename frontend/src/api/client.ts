const API_BASE = '/api';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

// Coding endpoints
export function getQuestions(filters?: { difficulty?: string; topic?: string; company?: string; frequency?: string; category?: string }) {
  const params = new URLSearchParams();
  if (filters?.difficulty) params.set('difficulty', filters.difficulty);
  if (filters?.topic) params.set('topic', filters.topic);
  if (filters?.company) params.set('company', filters.company);
  if (filters?.frequency) params.set('frequency', filters.frequency);
  if (filters?.category) params.set('category', filters.category);
  const qs = params.toString();
  return request<any[]>(`/coding/questions${qs ? '?' + qs : ''}`);
}

export function getFilters() {
  return request<{ algorithms: string[]; companies: string[]; categories: string[] }>('/coding/filters');
}

export function startCodingSession(questionId?: string, difficulty?: string, topic?: string) {
  return request<{ session_id: string; question: any; coach_message: string }>(
    '/coding/start',
    { method: 'POST', body: JSON.stringify({ question_id: questionId, difficulty, topic }) },
  );
}

export function sendCodingMessage(sessionId: string, message: string, code?: string, language?: string) {
  return request<{ response: string }>('/coding/chat', {
    method: 'POST',
    body: JSON.stringify({ session_id: sessionId, message, code, language }),
  });
}

export function submitSolution(sessionId: string, code: string, language: string, questionId: string) {
  return request<{
    stdout: string; stderr: string; exit_code: number; time_ms: number | null;
    passed: number; failed: number; total: number; all_passed: boolean;
  }>('/coding/submit', {
    method: 'POST',
    body: JSON.stringify({ session_id: sessionId, code, language, question_id: questionId }),
  });
}

export function generateQuestion(topic: string, difficulty: string, context?: string) {
  return request<any>('/coding/generate', {
    method: 'POST',
    body: JSON.stringify({ topic, difficulty, context: context || '' }),
  });
}

// System design endpoints
export function getDesignTopics() {
  return request<{ id: number; title: string }[]>('/system-design/topics');
}

export function startDesignSession(topic?: string) {
  return request<{ session_id: string; coach_message: string }>('/system-design/start', {
    method: 'POST',
    body: JSON.stringify({ topic }),
  });
}

export function sendDesignMessage(sessionId: string, message: string) {
  return request<{ response: string }>('/system-design/chat', {
    method: 'POST',
    body: JSON.stringify({ session_id: sessionId, message }),
  });
}

// User profile endpoints
export function createProfile(data: {
  name: string;
  email?: string;
  linkedin_url?: string;
  resume_text?: string;
  target_role?: string;
  target_companies?: string[];
  years_of_experience?: number;
}) {
  return request<any>('/users/profile', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export function getProfile(userId: string) {
  return request<any>(`/users/profile/${userId}`);
}

export function getProfiles() {
  return request<{ user_id: string; name: string }[]>('/users/profiles');
}

// Assessment endpoints
export function startAssessment(userId: string) {
  return request<any>(`/assessment/start?user_id=${userId}`, { method: 'POST' });
}

export function submitAssessment(userId: string, questionId: string, code: string, language: string) {
  return request<any>('/assessment/submit', {
    method: 'POST',
    body: JSON.stringify({ user_id: userId, question_id: questionId, code, language }),
  });
}

export function getAssessmentResults(userId: string) {
  return request<any>(`/assessment/results/${userId}`);
}

// Code execution
export function executeCode(code: string, language: string) {
  return request<{ stdout: string; stderr: string; exit_code: number; time_ms: number | null }>(
    '/execute/run',
    { method: 'POST', body: JSON.stringify({ code, language }) },
  );
}
