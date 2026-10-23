/**
 * AIET Voice Interaction Manager
 * Handles Web Speech Recognition (STT) and Speech Synthesis (TTS).
 */

class VoiceController {
  constructor(options = {}) {
    this.onTranscriptUpdate = options.onTranscriptUpdate || (() => {});
    this.onFinalTranscript = options.onFinalTranscript || (() => {});
    this.onStateChange = options.onStateChange || (() => {});
    this.onError = options.onError || (() => {});

    this.isListening = false;
    this.isSpeaking = false;
    this.speechEnabled = true;
    this.recognition = null;
    this.synth = window.speechSynthesis || null;
    this.preferredVoice = null;

    this.initRecognition();
    this.initVoices();
  }

  isRecognitionSupported() {
    return 'SpeechRecognition' in window || 'webkitSpeechRecognition' in window;
  }

  isSynthesisSupported() {
    return 'speechSynthesis' in window;
  }

  initRecognition() {
    if (!this.isRecognitionSupported()) {
      console.warn("Web Speech API is not supported in this browser.");
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    this.recognition = new SpeechRecognition();
    this.recognition.continuous = false;
    this.recognition.interimResults = true;
    this.recognition.lang = 'en-IN'; // Indian English default

    this.recognition.onstart = () => {
      this.isListening = true;
      this.stopSpeaking(); // Interrupt any ongoing speech output
      this.onStateChange({ status: 'listening' });
    };

    this.recognition.onresult = (event) => {
      let interimTranscript = '';
      let finalTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript;
        } else {
          interimTranscript += event.results[i][0].transcript;
        }
      }

      if (interimTranscript) {
        this.onTranscriptUpdate(interimTranscript);
      }

      if (finalTranscript) {
        this.onFinalTranscript(finalTranscript.trim());
      }
    };

    this.recognition.onerror = (event) => {
      console.warn("Speech recognition error:", event.error);
      this.isListening = false;
      this.onStateChange({ status: 'idle' });

      let userMsg = "Voice recognition error.";
      if (event.error === 'not-allowed' || event.error === 'permission-denied') {
        userMsg = "Microphone access was denied. Please allow microphone permissions in your browser settings to speak.";
      } else if (event.error === 'no-speech') {
        userMsg = "No speech detected. Please click the microphone and try speaking again.";
      } else if (event.error === 'network') {
        userMsg = "Network error during speech recognition. Please check your internet connection.";
      }
      this.onError(userMsg);
    };

    this.recognition.onend = () => {
      this.isListening = false;
      this.onStateChange({ status: 'idle' });
    };
  }

  initVoices() {
    if (!this.isSynthesisSupported()) return;

    const loadVoices = () => {
      const voices = this.synth.getVoices();
      // Look for natural English (India) or English (UK / US) voices
      this.preferredVoice = voices.find(v => v.lang.includes('en-IN') || v.name.includes('India')) ||
                            voices.find(v => v.lang.includes('en-US') && v.name.includes('Natural')) ||
                            voices.find(v => v.lang.includes('en-GB')) ||
                            voices.find(v => v.lang.startsWith('en')) ||
                            voices[0];
    };

    loadVoices();
    if (this.synth.onvoiceschanged !== undefined) {
      this.synth.onvoiceschanged = loadVoices;
    }
  }

  toggleListening() {
    if (this.isListening) {
      this.stopListening();
    } else {
      this.startListening();
    }
  }

  startListening() {
    if (!this.isRecognitionSupported()) {
      this.onError("Speech recognition is not supported in this browser. Please use Google Chrome, Edge, or enter your question using text.");
      return;
    }

    if (this.isListening) return;

    try {
      this.recognition.start();
    } catch (e) {
      console.warn("Speech recognition could not start:", e);
      this.stopListening();
    }
  }

  stopListening() {
    if (this.recognition && this.isListening) {
      try {
        this.recognition.stop();
      } catch (e) {
        console.warn("Error stopping recognition:", e);
      }
      this.isListening = false;
      this.onStateChange({ status: 'idle' });
    }
  }

  speak(text) {
    if (!this.speechEnabled || !this.isSynthesisSupported() || !text) return;

    this.stopSpeaking();

    // Clean markdown and URLs for natural spoken output
    const cleanText = text
      .replace(/https?:\/\/[^\s]+/g, '')
      .replace(/[*_#`~[\]]/g, '')
      .replace(/•/g, '')
      .replace(/\s+/g, ' ')
      .trim();

    if (!cleanText) return;

    const utterance = new SpeechSynthesisUtterance(cleanText);
    if (this.preferredVoice) {
      utterance.voice = this.preferredVoice;
    }
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    utterance.onstart = () => {
      this.isSpeaking = true;
      this.onStateChange({ status: 'speaking' });
    };

    utterance.onend = () => {
      this.isSpeaking = false;
      this.onStateChange({ status: 'idle' });
    };

    utterance.onerror = (e) => {
      console.warn("Speech synthesis error:", e);
      this.isSpeaking = false;
      this.onStateChange({ status: 'idle' });
    };

    this.synth.speak(utterance);
  }

  stopSpeaking() {
    if (this.synth && (this.synth.speaking || this.isSpeaking)) {
      this.synth.cancel();
      this.isSpeaking = false;
      this.onStateChange({ status: 'idle' });
    }
  }

  toggleSpeechOutput() {
    this.speechEnabled = !this.speechEnabled;
    if (!this.speechEnabled) {
      this.stopSpeaking();
    }
    return this.speechEnabled;
  }
}

window.VoiceController = VoiceController;
