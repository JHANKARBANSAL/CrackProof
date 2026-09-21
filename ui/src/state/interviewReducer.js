/**
 * Interview State Machine Reducer
 */

export const initialInterviewState = {
  status: "IDLE", // 'IDLE' | 'LOADING' | 'QUESTION' | 'RECORDING' | 'REVIEW' | 'EVALUATION' | 'REPORT'
  topic: "",
  interviewId: null,
  questionNumber: 1,
  questionText: "",
  recSeconds: 0,
  transcript: "",
  audioPath: null,
  audioBlob: null,
  evaluation: null,
  batchDone: false,
  report: null,
  loading: false,
  error: null
};

export function interviewReducer(state, action) {
  switch (action.type) {
    case "START_LOADING":
      return {
        ...initialInterviewState,
        status: "LOADING",
        topic: action.payload.topic,
        loading: true
      };

    case "START_INTERVIEW":
      return {
        ...initialInterviewState,
        status: "QUESTION",
        topic: action.payload.topic,
        interviewId: action.payload.interviewId,
        questionNumber: action.payload.questionNumber || 1,
        questionText: action.payload.questionText,
        loading: false
      };

    case "START_RECORDING":
      return {
        ...state,
        status: "RECORDING",
        recSeconds: 0,
        error: null
      };

    case "TICK_TIMER":
      return {
        ...state,
        recSeconds: state.recSeconds + 1
      };

    case "STOP_RECORDING":
      return {
        ...state,
        loading: true
      };

    case "RECORDING_FAILED":
      return {
        ...state,
        status: "QUESTION",
        loading: false,
        recSeconds: 0
      };

    case "SET_TRANSCRIPT":
      return {
        ...state,
        status: "REVIEW",
        loading: false,
        transcript: action.payload.transcript,
        audioPath: action.payload.audioPath,
        audioBlob: action.payload.audioBlob
      };

    case "UPDATE_TRANSCRIPT":
      return {
        ...state,
        transcript: action.payload
      };

    case "START_EVALUATION":
      return {
        ...state,
        loading: true,
        error: null
      };

    case "SET_EVALUATION":
      return {
        ...state,
        status: "EVALUATION",
        loading: false,
        evaluation: action.payload.evaluation,
        batchDone: action.payload.batchDone
      };

    case "SET_NEXT_QUESTION":
      return {
        ...state,
        status: "QUESTION",
        questionNumber: action.payload.questionNumber,
        questionText: action.payload.questionText,
        transcript: "",
        audioPath: null,
        audioBlob: null,
        evaluation: null,
        loading: false
      };

    case "SET_REPORT":
      return {
        ...state,
        status: "REPORT",
        report: action.payload,
        loading: false
      };

    case "SET_ERROR":
      return {
        ...state,
        loading: false,
        error: action.payload
      };

    case "RESET":
      return initialInterviewState;

    default:
      return state;
  }
}
