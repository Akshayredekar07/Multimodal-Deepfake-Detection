import React, { useEffect, useRef, useState } from 'react';
import {
  Brain, Menu, X, Github, Twitter, Linkedin,
  Upload, Play, AlertCircle, Mail, Lock, User,
  Shield, FileCheck, UserCheck, Slice as VoiceIcon,
  AlertTriangle, Zap, Code2, Phone, MapPin, Building2
} from 'lucide-react';
import Typed from 'typed.js';
import Slider from 'react-slick';
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

function App() {
  const [isMenuOpen, setIsMenuOpen] = React.useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [demoResult, setDemoResult] = useState<'real' | 'fake' | null>(null);
  const [result, setResult] = useState<{
    verdict: 'real' | 'fake' | null;
    confidence: number;
    time: string;
  } | null>(null);

  const typedRef = useRef(null);

  useEffect(() => {
    const typed = new Typed(typedRef.current, {
      strings: ['Fraud_', 'Generative AI_', 'Disinformation_', 'Voice Spoofing_'],
      typeSpeed: 70,
      backSpeed: 70,
      loop: true,
    });

    return () => {
      typed.destroy();
    };
  }, []);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setFile(file);
      setResult(null);
    }
  };

  const handleDetect = () => {
    setIsProcessing(true);
    setTimeout(() => {
      setResult({
        verdict: Math.random() > 0.5 ? 'real' : 'fake',
        confidence: Math.round(Math.random() * 30 + 70),
        time: '0.8 seconds'
      });
      setIsProcessing(false);
    }, 2000);
  };

  const handleDemoDetect = (type: string) => {
    setIsProcessing(true);
    setTimeout(() => {
      setDemoResult(Math.random() > 0.5 ? 'real' : 'fake');
      setIsProcessing(false);
    }, 1500);
  };

  const sliderSettings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 3000,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 2,
        }
      },
      {
        breakpoint: 640,
        settings: {
          slidesToShow: 1,
        }
      }
    ]
  };

  const AuthModal = ({ isLogin, onClose }: { isLogin: boolean; onClose: () => void }) => (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center">
      <div className="bg-[#1A1A1A] p-8 rounded-2xl w-full max-w-md relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-white"
        >
          <X className="h-6 w-6" />
        </button>
        <h2 className="text-2xl font-bold text-white mb-6">
          {isLogin ? 'Welcome Back' : 'Create Account'}
        </h2>
        <form className="space-y-4">
          {!isLogin && (
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-400 mb-1">
                Full Name
              </label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  id="name"
                  className="w-full bg-[#232323] border border-gray-700 rounded-lg py-2 pl-10 pr-4 text-white focus:ring-2 focus:ring-[#6C5DD3] focus:border-transparent"
                  placeholder="John Doe"
                />
              </div>
            </div>
          )}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-400 mb-1">
              Email
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="email"
                id="email"
                className="w-full bg-[#232323] border border-gray-700 rounded-lg py-2 pl-10 pr-4 text-white focus:ring-2 focus:ring-[#6C5DD3] focus:border-transparent"
                placeholder="you@example.com"
              />
            </div>
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-400 mb-1">
              Password
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="password"
                id="password"
                className="w-full bg-[#232323] border border-gray-700 rounded-lg py-2 pl-10 pr-4 text-white focus:ring-2 focus:ring-[#6C5DD3] focus:border-transparent"
                placeholder="••••••••"
              />
            </div>
          </div>
          <button
            type="submit"
            className="w-full bg-[#6C5DD3] hover:bg-[#8A7BF7] text-white font-medium py-2 px-4 rounded-lg transition-colors"
          >
            {isLogin ? 'Sign In' : 'Create Account'}
          </button>
        </form>
        <p className="mt-4 text-center text-gray-400">
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <button
            onClick={() => {
              onClose();
              isLogin ? setShowRegister(true) : setShowLogin(true);
            }}
            className="text-[#6C5DD3] hover:text-[#8A7BF7]"
          >
            {isLogin ? 'Sign up' : 'Sign in'}
          </button>
        </p>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-[#0D0D0D]">
      {showLogin && <AuthModal isLogin={true} onClose={() => setShowLogin(false)} />}
      {showRegister && <AuthModal isLogin={false} onClose={() => setShowRegister(false)} />}

      {/* Header */}
      <header className="fixed w-full bg-[#0D0D0D]/80 backdrop-blur-md z-50 border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="flex justify-between items-center py-4">
            {/* Left side */}
            <div className="flex items-center space-x-8">
              <a href="/" className="flex items-center space-x-2">
                <Brain className="h-8 w-8 text-[#6C5DD3]" />
                <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[#6C5DD3] to-[#8A7BF7]">Detectify.ai</span>
              </a>
              <nav className="hidden md:flex items-center space-x-8">
                <a href="#how-it-works" className="text-gray-300 hover:text-white">How It Works</a>
                <a href="#detect" className="text-gray-300 hover:text-white">Detect</a>
                <a href="#contact" className="text-gray-300 hover:text-white">Contact Us</a>
              </nav>
            </div>

            {/* Right side */}
            <div className="hidden md:flex items-center space-x-6">
              <button
                onClick={() => setShowLogin(true)}
                className="text-gray-300 hover:text-white"
              >
                Log in
              </button>
              <button
                onClick={() => setShowRegister(true)}
                className="bg-[#6C5DD3] hover:bg-[#8A7BF7] text-white px-6 py-2 rounded-md transition-colors"
              >
                Get Started Now
              </button>
            </div>

            {/* Mobile menu button */}
            <button
              className="md:hidden"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? (
                <X className="h-6 w-6 text-gray-300" />
              ) : (
                <Menu className="h-6 w-6 text-gray-300" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {isMenuOpen && (
          <div className="md:hidden bg-[#0D0D0D]">
            <div className="px-2 pt-2 pb-3 space-y-1">
              <a href="#how-it-works" className="block px-3 py-2 text-gray-300 hover:text-white">How It Works</a>
              <a href="#contact" className="block px-3 py-2 text-gray-300 hover:text-white">Contact Us</a>
              <button
                onClick={() => setShowLogin(true)}
                className="block w-full text-left px-3 py-2 text-gray-300 hover:text-white"
              >
                Log in
              </button>
              <button
                onClick={() => setShowRegister(true)}
                className="block w-full text-left px-3 py-2 text-[#6C5DD3] hover:text-[#8A7BF7]"
              >
                Get Started Now
              </button>
            </div>
          </div>
        )}
      </header>

      {/* Hero Section */}
      <main>
        <div className="relative">
          <div className="absolute inset-0 bg-gradient-to-br from-[#0D0D0D] via-[#1A1A1A] to-[#0D0D0D] z-0" />
          <div className="max-w-7xl mx-auto px-4 sm:px-6 pt-32 pb-16 relative z-10">
            <div className="text-center">
              <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold mb-4">
                <span className="text-white">Detect</span>
              </h1>
              <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-8">
                <span ref={typedRef} className="bg-clip-text text-transparent bg-gradient-to-r from-[#6C5DD3] to-[#8A7BF7]"></span>
              </h2>
              <p className="max-w-2xl mx-auto text-xl mt-8 text-gray-300 mb-10">
                Detectify.ai's multi-model and multimodal deepfake detection platform helps enterprises
                and governments detect AI-generated content at scale.
              </p>
              <div  className='flex gap-8 mt-12 items-center justify-center'>
              <a href="#detect" 
                  className="bg-[#6C5DD3] text-white px-8 py-3 rounded-lg hover:bg-[#8A7BF7] transition-colors"
                >
                  Try it Now
                </a>
                <a href="#how-it-works" 
                  className="text-gray-300  hover:text-white"
                >
                  Learn More →
                </a>
              </div>
            </div>

            {/* Demo Slider Section */}
            <div className="mt-16 mb-24">
              <Slider {...sliderSettings}>
                {/* Real Images */}
                <div className="px-4">
                  <div className="relative group">
                    <img
                      src="https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=800&q=80"
                      alt="Real person"
                      className="rounded-lg h-64 w-full object-cover transition-transform duration-300 group-hover:scale-105"
                    />
                    <p className="text-center text-white mt-4 text-lg font-semibold">Real Image</p>
                    <p className="text-center text-green-400 text-sm">Verified Authentic</p>
                  </div>
                </div>
                <div className="px-4">
                  <div className="relative group">
                    <img
                      src="https://images.unsplash.com/photo-1552058544-f2b08422138a?auto=format&fit=crop&w=800&q=80"
                      alt="Real person"
                      className="rounded-lg h-64 w-full object-cover transition-transform duration-300 group-hover:scale-105"
                    />
                    <p className="text-center text-white mt-4 text-lg font-semibold">Real Image</p>
                    <p className="text-center text-green-400 text-sm">Verified Authentic</p>
                  </div>
                </div>
                {/* AI Generated Images */}
                <div className="px-4">
                  <div className="relative group">
                    <img
                      src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=800&q=80"
                      alt="AI Generated"
                      className="rounded-lg h-64 w-full object-cover transition-transform duration-300 group-hover:scale-105 opacity-90"
                    />
                    <p className="text-center text-white mt-4 text-lg font-semibold">AI Generated</p>
                    <p className="text-center text-red-400 text-sm">Detected as Fake</p>
                  </div>
                </div>
                <div className="px-4">
                  <div className="relative group">
                    <img
                      src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=800&q=80"
                      alt="AI Generated"
                      className="rounded-lg h-64 w-full object-cover transition-transform duration-300 group-hover:scale-105 opacity-90"
                    />
                    <p className="text-center text-white mt-4 text-lg font-semibold">AI Generated</p>
                    <p className="text-center text-red-400 text-sm">Detected as Fake</p>
                  </div>
                </div>
              </Slider>
            </div>

            {/* Multimodal Demo Detection Section */}
            <div className="max-w-6xl mx-auto bg-[#1A1A1A] rounded-2xl p-8 shadow-xl mb-24">
              <div className="text-center mb-12">
                <h3 className="text-3xl font-bold text-white mb-4">Experience Multimodal Detection</h3>
                <p className="text-gray-400">Test our AI's ability to detect deepfakes across different media types</p>
              </div>

              <div className="grid md:grid-cols-3 gap-8">
                {/* Audio Detection */}
                <div className="bg-[#232323] p-6 rounded-xl">
                  <div className="text-center mb-6">
                    <VoiceIcon className="h-12 w-12 text-[#6C5DD3] mx-auto mb-4" />
                    <h4 className="text-xl font-semibold text-white mb-2">Audio Detection</h4>
                    <p className="text-gray-400 text-sm">Detect AI-generated voices and audio deepfakes</p>
                  </div>
                  <div className="flex justify-center mb-4">
                    <audio
                      controls
                      className="w-full"
                      src="https://example.com/demo-audio.mp3"
                    >
                      Your browser does not support the audio element.
                    </audio>
                  </div>
                  <button
                    onClick={() => handleDemoDetect('audio')}
                    className="w-full bg-[#6C5DD3] hover:bg-[#8A7BF7] text-white py-2 rounded-lg transition-colors"
                  >
                    Analyze Audio
                  </button>
                </div>

                {/* Image Detection */}
                <div className="bg-[#232323] p-6 rounded-xl">
                  <div className="text-center mb-6">
                    <FileCheck className="h-12 w-12 text-[#6C5DD3] mx-auto mb-4" />
                    <h4 className="text-xl font-semibold text-white mb-2">Image Detection</h4>
                    <p className="text-gray-400 text-sm">Identify AI-generated and manipulated images</p>
                  </div>
                  <div className="mb-4">
                    <img
                      src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=800&q=80"
                      alt="Demo face"
                      className="w-full h-48 object-cover rounded-lg"
                    />
                  </div>
                  <button
                    onClick={() => handleDemoDetect('image')}
                    className="w-full bg-[#6C5DD3] hover:bg-[#8A7BF7] text-white py-2 rounded-lg transition-colors"
                  >
                    Analyze Image
                  </button>
                </div>

                {/* Video Detection */}
                <div className="bg-[#232323] p-6 rounded-xl">
                  <div className="text-center mb-6">
                    <Play className="h-12 w-12 text-[#6C5DD3] mx-auto mb-4" />
                    <h4 className="text-xl font-semibold text-white mb-2">Video Detection</h4>
                    <p className="text-gray-400 text-sm">Spot deepfake videos and manipulated content</p>
                  </div>
                  <div className="mb-4">
                    <video
                      className="w-full h-48 object-cover rounded-lg"
                      controls
                    >
                      <source src="https://example.com/demo-video.mp4" type="video/mp4" />
                      Your browser does not support the video tag.
                    </video>
                  </div>
                  <button
                    onClick={() => handleDemoDetect('video')}
                    className="w-full bg-[#6C5DD3] hover:bg-[#8A7BF7] text-white py-2 rounded-lg transition-colors"
                  >
                    Analyze Video
                  </button>
                </div>
              </div>
            </div>

            {/* Upload & Detection Section */}
            <div id="detect" className="mt-24 mb-24 bg-[#1A1A1A] rounded-2xl p-8 shadow-xl">
              <div className="text-center mb-12">
                <h2 className="text-3xl font-bold text-white mb-4">Upload & Detect Deepfakes</h2>
                <p className="text-gray-400">Upload an image, video, or audio file to analyze whether it's AI-generated or real.</p>
              </div>

              <div className="grid md:grid-cols-2 gap-8">
                {/* Left Side: Upload */}
                <div className="space-y-6">
                  <div className="border-2 border-dashed border-gray-700 rounded-xl p-8 text-center hover:border-[#6C5DD3] transition-colors group">
                    <input
                      type="file"
                      id="file-upload"
                      className="hidden"
                      onChange={handleFileUpload}
                      accept="image/*,video/*,audio/*"
                    />
                    <label
                      htmlFor="file-upload"
                      className="cursor-pointer space-y-4 flex flex-col items-center"
                    >
                      <Upload className="h-12 w-12 text-[#6C5DD3] group-hover:scale-110 transition-transform" />
                      <div className="space-y-2">
                        <p className="text-white font-medium">Drag & drop or click to upload</p>
                        <p className="text-sm text-gray-400">Supports images, videos, and audio files</p>
                      </div>
                    </label>
                  </div>

                  {file && (
                    <div className="text-center">
                      <p className="text-gray-300 mb-4">Selected file: {file.name}</p>
                      <button
                        onClick={handleDetect}
                        disabled={isProcessing}
                        className={`w-full py-3 rounded-full font-medium ${isProcessing
                            ? 'bg-gray-600 cursor-not-allowed'
                            : 'bg-[#6C5DD3] hover:bg-[#8A7BF7]'
                          } text-white transition-colors`}
                      >
                        {isProcessing ? 'Processing...' : 'Detect Fake'}
                      </button>
                    </div>
                  )}
                </div>

                {/* Right Side: Results */}
                <div className="bg-[#232323] rounded-xl p-6">
                  <h3 className="text-xl font-semibold text-white mb-6">Detection Results</h3>

                  {result ? (
                    <div className="space-y-6">
                      <div className={`p-4 rounded-lg ${result.verdict === 'real' ? 'bg-green-900/20' : 'bg-red-900/20'
                        }`}>
                        <div className="flex items-center space-x-3">
                          <AlertCircle className={`h-6 w-6 ${result.verdict === 'real' ? 'text-green-400' : 'text-red-400'
                            }`} />
                          <span className="text-lg font-medium text-white capitalize">
                            {result.verdict}
                          </span>
                        </div>
                      </div>

                      <div className="space-y-4">
                        <div>
                          <p className="text-gray-400 mb-1">Confidence Score</p>
                          <div className="h-2 bg-gray-700 rounded-full">
                            <div
                              className={`h-full rounded-full ${result.verdict === 'real' ? 'bg-green-500' : 'bg-red-500'
                                }`}
                              style={{ width: `${result.confidence}%` }}
                            />
                          </div>
                          <p className="text-right text-sm text-gray-400 mt-1">{result.confidence}%</p>
                        </div>

                        <div>
                          <p className="text-gray-400">Detection Time</p>
                          <p className="text-white">{result.time}</p>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center text-gray-400 py-12">
                      <AlertCircle className="h-12 w-12 mx-auto mb-4 opacity-50" />
                      <p>Upload a file to see detection results</p>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* How It Works Section */}
            <div id="how-it-works" className="mb-24">
              <h2 className="text-3xl font-bold text-white text-center mb-16">How It Works</h2>
              <div className="relative">
                {/* Timeline Line */}
                <div className="absolute left-1/2 transform -translate-x-1/2 h-full w-1 bg-[#6C5DD3] opacity-20"></div>

                {/* Timeline Items */}
                <div className="space-y-24">
                  {/* Step 1 */}
                  <div className="relative">
                    <div className="absolute left-1/2 transform -translate-x-1/2 -mt-3">
                      <div className="w-8 h-8 bg-[#6C5DD3] rounded-full flex items-center justify-center">
                        <span className="text-white font-bold">1</span>
                      </div>
                    </div>
                    <div className="ml-auto mr-[calc(50%+2rem)] md:mr-[calc(50%+4rem)] p-6 bg-[#1A1A1A] rounded-xl">
                      <h3 className="text-xl font-bold text-white mb-4">Upload Media</h3>
                      <ul className="space-y-2 text-gray-400">
                        <li className="flex items-start space-x-2">
                          <Upload className="h-5 w-5 text-[#6C5DD3] mt-1 flex-shrink-0" />
                          <span>Upload an image, video, or audio file for analysis</span>
                        </li>
                        <li className="flex items-start space-x-2">
                          <FileCheck className="h-5 w-5 text-[#6C5DD3] mt-1 flex-shrink-0" />
                          <span>Supports multiple formats for deepfake detection</span>
                        </li>
                      </ul>
                    </div>
                  </div>

                  {/* Step 2 */}
                  <div className="relative">
                    <div className="absolute left-1/2 transform -translate-x-1/2 -mt-3">
                      <div className="w-8 h-8 bg-[#6C5DD3] rounded-full flex items-center justify-center">
                        <span className="text-white font-bold">2</span>
                      </div>
                    </div>
                    <div className="mr-auto ml-[calc(50%+2rem)] md:ml-[calc(50%+4rem)] p-6 bg-[#1A1A1A] rounded-xl">
                      <h3 className="text-xl font-bold text-white mb-4">AI Detection in Action</h3>
                      <ul className="space-y-2 text-gray-400">
                        <li className="flex items-start space-x-2">
                          <Brain className="h-5 w-5 text-[#6C5DD3] mt-1 flex-shrink-0" />
                          <span>Our advanced AI scans the media using deep learning models</span>
                        </li>
                        <li className="flex items-start space-x-2">
                          <AlertCircle className="h-5 w-5 text-[#6C5DD3] mt-1 flex-shrink-0" />
                          <span>Analyzes patterns, inconsistencies, and digital manipulations</span>
                        </li>
                      </ul>
                    </div>
                  </div>

                  {/* Step 3 */}
                  <div className="relative">
                    <div className="absolute left-1/2 transform -translate-x-1/2 -mt-3">
                      <div className="w-8 h-8 bg-[#6C5DD3] rounded-full flex items-center justify-center">
                        <span className="text-white font-bold">3</span>
                      </div>
                    </div>
                    <div className="ml-auto mr-[calc(50%+2rem)] md:mr-[calc(50%+4rem)] p-6 bg-[#1A1A1A] rounded-xl">
                      <h3 className="text-xl font-bold text-white mb-4">Get Instant Results</h3>
                      <ul className="space-y-2 text-gray-400">
                        <li className="flex items-start space-x-2">
                          <Zap className="h-5 w-5 text-[#6C5DD3] mt-1 flex-shrink-0" />
                          <span>The system provides a confidence score indicating if the content is real or fake</span>
                        </li>
                        <li className="flex items-start space-x-2">
                          <AlertTriangle className="h-5 w-5 text-[#6C5DD3] mt-1 flex-shrink-0" />
                          <span>Visual reports highlight detected anomalies</span>
                        </li>
                      </ul>
                    </div>
                  </div>

                  {/* Step 4 */}
                  <div className="relative">
                    <div className="absolute left-1/2 transform -translate-x-1/2 -mt-3">
                      <div className="w-8 h-8 bg-[#6C5DD3] rounded-full flex items-center justify-center">
                        <span className="text-white font-bold">4</span>
                      </div>
                    </div>
                    <div className="mr-auto ml-[calc(50%+2rem)] md:ml-[calc(50%+4rem)] p-6 bg-[#1A1A1A] rounded-xl">
                      <h3 className="text-xl font-bold text-white mb-4">Secure & Reliable</h3>
                      <ul className="space-y-2 text-gray-400">
                        <li className="flex items-start space-x-2">
                          <Shield className="h-5 w-5 text-[#6C5DD3] mt-1 flex-shrink-0" />
                          <span>Uses cutting-edge AI models for high accuracy</span>
                        </li>
                        <li className="flex items-start space-x-2">
                          <Lock className="h-5 w-5 text-[#6C5DD3] mt-1 flex-shrink-0" />
                          <span>Ensures data privacy and secure processing</span>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Industries We Secure Section */}
            <div className="mb-24">
              <h2 className="text-3xl font-bold text-white text-center mb-16">Industries We Secure</h2>
              <div className="grid md:grid-cols-3 gap-8">
                {/* Media & Content */}
                <div className="bg-[#1A1A1A] p-8 rounded-2xl transform hover:scale-105 transition-transform duration-300">
                  <FileCheck className="h-12 w-12 text-[#6C5DD3] mb-6" />
                  <h3 className="text-xl font-bold text-white mb-4">Media & Content Authenticity</h3>
                  <ul className="space-y-3 text-gray-400">
                    <li className="flex items-start space-x-2">
                      <AlertCircle className="h-5 w-5 text-[#6C5DD3] mt-1 flex-shrink-0" />
                      <span>Synthesized Voice Detection</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <AlertCircle className="h-5 w-5 text-[#6C5DD3] mt-1 flex-shrink-0" />
                      <span>Content Integrity & Authenticity Verification</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <AlertCircle className="h-5 w-5 text-[#6C5DD3] mt-1 flex-shrink-0" />
                      <span>Deepfake & AI-Generated Disinformation Protection</span>
                    </li>
                  </ul>
                </div>

                {/* Finance & Cybersecurity */}
                <div className="bg-[#1A1A1A] p-8 rounded-2xl transform hover:scale-105 transition-transform duration-300">
                  <Shield className="h-12 w-12 text-[#6C5DD3] mb-6" />
                  <h3 className="text-xl font-bold text-white mb-4">Finance & Cybersecurity</h3>
                  <ul className="space-y-3 text-gray-400">
                    <li className="flex items-start space-x-2">
                      <AlertCircle className="h-5 w-5 text-[#6C5DD3] mt-1 flex-shrink-0" />
                      <span>AI-Based Voice Cloning Detection</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <AlertCircle className="h-5 w-5 text-[#6C5DD3] mt-1 flex-shrink-0" />
                      <span>Fraudulent Document & ID Verification</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <AlertCircle className="h-5 w-5 text-[#6C5DD3] mt-1 flex-shrink-0" />
                      <span>Advanced KYC Protection</span>
                    </li>
                  </ul>
                </div>

                {/* Government & Public Safety */}
                <div className="bg-[#1A1A1A] p-8 rounded-2xl transform hover:scale-105 transition-transform duration-300">
                  <UserCheck className="h-12 w-12 text-[#6C5DD3] mb-6" />
                  <h3 className="text-xl font-bold text-white mb-4">Government & Public Safety</h3>
                  <ul className="space-y-3 text-gray-400">
                    <li className="flex items-start space-x-2">
                      <AlertCircle className="h-5 w-5 text-[#6C5DD3] mt-1 flex-shrink-0" />
                      <span>Voice Impersonation & Synthetic Speech Detection</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <AlertCircle className="h-5 w-5 text-[#6C5DD3] mt-1 flex-shrink-0" />
                      <span>Detection of Fraudulent Communications</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <AlertCircle className="h-5 w-5 text-[#6C5DD3] mt-1 flex-shrink-0" />
                      <span>Combatting Disinformation Campaigns</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Why Choose Detectify.ai Section */}
            {/* <div className="mb-24">
              <h2 className="text-3xl font-bold text-white text-center mb-16">Why Choose Detectify.ai?</h2>
              <div className="grid md:grid-cols-3 gap-8">
                <div className="bg-[#1A1A1A] p-8 rounded-2xl transform hover:scale-105 transition-transform duration-300">
                  <Brain className="h-12 w-12 text-[#6C5DD3] mb-6" />
                  <h3 className="text-xl font-bold text-white mb-4">State-of-the-art AI Models</h3>
                  <p className="text-gray-400">Advanced detection models trained on multimodal data for superior accuracy</p>
                </div>
                <div className="bg-[#1A1A1A] p-8 rounded-2xl transform hover:scale-105 transition-transform duration-300">
                  <Zap className="h-12 w-12 text-[#6C5DD3] mb-6" />
                  <h3 className="text-xl font-bold text-white mb-4">Real-time Analysis</h3>
                  <p className="text-gray-400">Scalable deepfake analysis for enterprises and governments</p>
                </div>
                <div className="bg-[#1A1A1A] p-8 rounded-2xl transform hover:scale-105 transition-transform duration-300">
                  <Code2 className="h-12 w-12 text-[#6C5DD3] mb-6" />
                  <h3 className="text-xl font-bold text-white mb-4">Seamless Integration</h3>
                  <p className="text-gray-400">Easy API integration for fraud prevention and content verification</p>
                </div>
              </div>
            </div> */}

            {/* Contact Us Section */}
            <div id="contact" className="mb-8 bg-[#1A1A1A] rounded-2xl p-8 shadow-xl">
              <h2 className="text-3xl font-bold text-white text-center mb-12">Contact Us</h2>
              <div className="">
                {/* Contact Information */}
                <div className="flex flex-row justify-between space-x-12 px-20 pb-8">
                  <div className="flex space-x-4">
                    <Mail className="h-6 w-6 text-[#6C5DD3] mt-1" />
                    <div>
                      <h3 className="text-white font-semibold mb-2">Email</h3>
                      <p className="text-gray-400">support@detectify.ai</p>
                      <p className="text-gray-400">business@detectify.ai (Business)</p>
                      <p className="text-gray-400">press@detectify.ai (Media)</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-4">
                    <Phone className="h-6 w-6 text-[#6C5DD3] mt-1" />
                    <div>
                      <h3 className="text-white font-semibold mb-2">Phone</h3>
                      <p className="text-gray-400">+91-9999-999999</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-4">
                    <MapPin className="h-6 w-6 text-[#6C5DD3] mt-1" />
                    <div>
                      <h3 className="text-white font-semibold mb-2">Address</h3>
                      <p className="text-gray-400">Pune, India</p>
                    </div>
                  </div>
                </div>

                {/* Social Links */}
                {/* <div className="bg-[#1A1A1A] p-6 rounded-xl">
                  <h3 className="text-xl font-bold text-white mb-6">Connect With Us</h3>
                  <div className="space-y-4">
                    <a href="#linkedin" className="flex items-center space-x-4 text-gray-400 hover:text-white transition-colors">
                      <Linkedin className="h-6 w-6" />
                      <span>LinkedIn</span>
                    </a>
                    <a href="#twitter" className="flex items-center space-x-4 text-gray-400 hover:text-white transition-colors">
                      <Twitter className="h-6 w-6" />
                      <span>Twitter/X</span>
                    </a>
                    <a href="#github" className="flex items-center space-x-4 text-gray-400 hover:text-white transition-colors">
                      <Github className="h-6 w-6" />
                      <span>GitHub</span>
                    </a>
                  </div>
                  <div className="mt-8 pt-8 border-t border-gray-700">
                    <h4 className="text-white font-semibold mb-4">Business Hours</h4>
                    <p className="text-gray-400">Monday - Friday: 9:00 AM - 6:00 PM IST</p>
                    <p className="text-gray-400">Saturday - Sunday: Closed</p>
                  </div>
                </div> */}
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-[#0D0D0D] border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <a href="/" className="flex items-center space-x-2">
                <Brain className="h-8 w-8 text-[#6C5DD3]" />
                <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[#6C5DD3] to-[#8A7BF7]">
                  Detectify.ai
                </span>
              </a>
              <p className="text-gray-400">
                Protecting truth in the age of AI
              </p>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Product</h3>
              <ul className="space-y-2">
                <li><a href="#features" className="text-gray-400 hover:text-white">Features</a></li>
                <li><a href="#pricing" className="text-gray-400 hover:text-white">Pricing</a></li>
                <li><a href="#demo" className="text-gray-400 hover:text-white">Request Demo</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Company</h3>
              <ul className="space-y-2">
                <li><a href="#careers" className="text-gray-400 hover:text-white">Careers</a></li>
                <li><a href="#contact" className="text-gray-400 hover:text-white">Contact</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Legal</h3>
              <ul className="space-y-2">
                <li><a href="#privacy" className="text-gray-400 hover:text-white">Privacy Policy</a></li>
                <li><a href="#terms" className="text-gray-400 hover:text-white">Terms of Service</a></li>
              </ul>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400">© 2025 Detectify.ai. All rights reserved.</p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a href="#twitter" className="text-gray-400 hover:text-white transition-colors">
                <Twitter className="h-6 w-6" />
              </a>
              <a href="#github" className="text-gray-400 hover:text-white transition-colors">
                <Github className="h-6 w-6" />
              </a>
              <a href="#linkedin" className="text-gray-400 hover:text-white transition-colors">
                <Linkedin className="h-6 w-6" />
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;