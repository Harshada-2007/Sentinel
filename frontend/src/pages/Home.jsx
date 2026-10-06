import { Link } from 'react-router-dom'
import { 
  ShieldCheck, Activity, GitBranch, Lightbulb, ArrowRight, 
  PlayCircle, BarChart3, Database, Lock, Zap, CheckCircle2, ChevronRight
} from 'lucide-react'

const FEATURES = [
  { icon: Activity,   title: 'Predict disruptions',   body: 'AI analyzes supplier reliability, lead times, and external signals to flag risk before it hits.' },
  { icon: GitBranch,  title: 'See the blast radius',  body: 'Trace any event through suppliers, products, warehouses, and orders — all the way to rupees at risk.' },
  { icon: Lightbulb,  title: 'Get the best action',   body: 'An optimizer compares backup suppliers, inventory transfers, and reorder timing by cost and impact.' },
  { icon: ShieldCheck,title: 'Log every decision',    body: 'Every accepted plan is written to an immutable audit trail for compliance and review.' },
]

const STEPS = [
  { step: '01', title: 'Ingest & Monitor', desc: 'Connect your ERP, WMS, and external news feeds. Sentinel continuously monitors for anomalies.', icon: Database },
  { step: '02', title: 'Analyze Impact', desc: 'When a disruption hits, visualize the cascading effect from the factory floor to the final customer.', icon: BarChart3 },
  { step: '03', title: 'Simulate Actions', desc: 'Run "what-if" scenarios. Test backup suppliers, inventory transfers, and pricing strategies safely.', icon: Zap },
  { step: '04', title: 'Execute & Audit', desc: 'Deploy the optimal mitigation plan with one click. Every action is logged for compliance.', icon: Lock },
]

export default function Home() {
  return (
    <div className="min-h-screen bg-ink-900 text-slate-200 overflow-x-hidden selection:bg-accent/30 selection:text-white">
      
      {/* --- NAVIGATION --- */}
      <header className="h-20 border-b border-ink-600 flex items-center justify-between px-6 md:px-12 bg-ink-900/80 backdrop-blur-xl fixed top-0 w-full z-50 transition-all duration-300">
        <div className="flex items-center gap-3">
          <span className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-glow">
            <ShieldCheck className="text-white" size={22} />
          </span>
          <div className="leading-tight">
            <div className="text-white font-bold text-lg tracking-wide">Sentinel</div>
            <div className="text-[10px] text-slate-400 font-medium uppercase tracking-widest">Control Tower</div>
          </div>
        </div>
        
        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-300">
          <a href="#features" className="hover:text-white transition-colors">Features</a>
          <a href="#how-it-works" className="hover:text-white transition-colors">How it Works</a>
          <a href="#about" className="hover:text-white transition-colors">About</a>
        </nav>

        <nav className="flex items-center gap-4">
          <Link to="/login" className="hidden md:block text-sm font-medium text-slate-300 hover:text-white transition-colors">Sign in</Link>
          <Link to="/login" className="btn text-sm px-4 py-2 shadow-lg shadow-accent/20">Get started <ArrowRight size={16} /></Link>
        </nav>
      </header>

      {/* --- HERO SECTION --- */}
      <section className="relative pt-40 pb-24 md:pt-52 md:pb-32 px-6 flex flex-col items-center text-center">
        {/* Background Gradients */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[500px] bg-blue-500/10 blur-[120px] rounded-full pointer-events-none -z-10" />
        <div className="absolute top-40 right-10 w-[400px] h-[400px] bg-indigo-500/10 blur-[100px] rounded-full pointer-events-none -z-10" />

        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-medium mb-8 backdrop-blur-sm animate-fade-in-up">
          <span className="w-2 h-2 rounded-full bg-blue-400 animate-pulse" />
          AI-powered Supply Chain Intelligence
        </div>
        
        <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white leading-[1.1] max-w-4xl mx-auto animate-fade-in-up animation-delay-100">
          Predict supply chain disruptions <br className="hidden md:block" />
          <span className="bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent">
            before they cost you a thing.
          </span>
        </h1>
        
        <p className="text-slate-400 text-lg md:text-xl mt-8 max-w-2xl mx-auto leading-relaxed animate-fade-in-up animation-delay-200">
          Sentinel watches your suppliers, warehouses, and orders — predicts what breaks next,
          quantifies the impact in rupees, and tells you the cheapest action to keep operations running.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-12 animate-fade-in-up animation-delay-300">
          <Link to="/login" className="btn text-base px-8 py-4 w-full sm:w-auto shadow-xl shadow-blue-500/20 hover:scale-105 transition-transform">
            Open the Control Tower <ArrowRight size={18} />
          </Link>
          <a href="#how-it-works" className="px-8 py-4 w-full sm:w-auto rounded-lg border border-ink-600 bg-ink-800/50 hover:bg-ink-800 text-white font-medium flex items-center justify-center gap-2 transition-all">
            <PlayCircle size={18} /> See how it works
          </a>
        </div>
      </section>

      {/* --- TRUST / STATS STRIP ---
      <section className="border-y border-ink-600 bg-ink-800/30 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-6 py-10 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {[
            { value: '99.9%', label: 'Uptime SLA' },
            { value: '₹0', label: 'Cost to start' },
            { value: '< 2s', label: 'Impact Analysis' },
            { value: '24/7', label: 'Automated Monitoring' }
          ].map((stat, i) => (
            <div key={i} className="flex flex-col items-center">
              <span className="text-2xl md:text-3xl font-bold text-white mb-1">{stat.value}</span>
              <span className="text-xs md:text-sm text-slate-500 uppercase tracking-wider font-medium">{stat.label}</span>
            </div>
          ))}
        </div>
      </section> */}

      {/* --- FEATURES SECTION --- */}
      <section id="features" className="max-w-7xl mx-auto px-6 py-24 md:py-32">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-white tracking-tight mb-4">One tower. Every signal.</h2>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">From detection to decision, in one place. We replace spreadsheets and gut feelings with hard data.</p>
        </div>
        
        <div className="grid md:grid-cols-2 gap-6">
          {FEATURES.map(({ icon: Icon, title, body }, idx) => (
            <div key={title} className="group relative p-8 rounded-2xl bg-ink-800/40 border border-ink-600 hover:border-blue-500/50 hover:bg-ink-800/80 transition-all duration-300">
              <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/5 blur-[50px] rounded-full group-hover:bg-blue-500/10 transition-colors" />
              <span className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 mb-6 group-hover:scale-110 transition-transform">
                <Icon size={24} />
              </span>
              <h3 className="text-xl font-semibold text-white mb-3">{title}</h3>
              <p className="text-slate-400 leading-relaxed">{body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* --- HOW IT WORKS SECTION --- */}
      <section id="how-it-works" className="bg-ink-800/20 border-y border-ink-600 py-24 md:py-32">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between items-end mb-16 gap-6">
            <div className="max-w-2xl">
              <h2 className="text-3xl md:text-5xl font-bold text-white tracking-tight mb-4">How Sentinel Works</h2>
              <p className="text-slate-400 text-lg">A seamless loop from raw data to executed action. No more silos.</p>
            </div>
            <Link to="/login" className="text-blue-400 hover:text-blue-300 font-medium flex items-center gap-2 transition-colors">
              Try the simulator <ChevronRight size={18} />
            </Link>
          </div>

          <div className="grid md:grid-cols-4 gap-8 relative">
            {/* Connecting Line (Desktop) */}
            <div className="hidden md:block absolute top-12 left-0 w-full h-0.5 bg-gradient-to-r from-blue-500/0 via-blue-500/50 to-blue-500/0 -z-10" />
            
            {STEPS.map((item, idx) => (
              <div key={idx} className="relative flex flex-col items-start">
                <div className="w-24 h-24 rounded-2xl bg-ink-900 border border-ink-600 flex items-center justify-center mb-6 shadow-xl relative z-10">
                  <item.icon size={32} className="text-blue-400" />
                  <span className="absolute -top-3 -right-3 w-8 h-8 rounded-full bg-blue-600 text-white text-xs font-bold flex items-center justify-center border-4 border-ink-900">
                    {item.step}
                  </span>
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">{item.title}</h3>
                <p className="text-sm text-slate-400 leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* --- ABOUT SECTION --- */}
      <section id="about" className="max-w-7xl mx-auto px-6 py-24 md:py-32">
        <div className="grid md:grid-cols-2 gap-16 items-center">
          <div>
            <h2 className="text-3xl md:text-5xl font-bold text-white tracking-tight mb-6">Built for modern, fragile supply chains.</h2>
            <p className="text-slate-400 text-lg leading-relaxed mb-6">
              Global supply chains are more interconnected and fragile than ever. A single factory fire in Taipei or a port strike in Vietnam can halt your operations for weeks. 
            </p>
            <p className="text-slate-400 text-lg leading-relaxed mb-8">
              Sentinel was built to give supply chain leaders a God's-eye view of their operations. We combine real-time data ingestion with advanced predictive AI to not only tell you what is happening, but exactly what to do about it.
            </p>
            <ul className="space-y-4">
              {['Enterprise-grade security', 'Seamless ERP integrations', 'Explainable AI recommendations'].map((item, i) => (
                <li key={i} className="flex items-center gap-3 text-slate-300">
                  <CheckCircle2 size={20} className="text-blue-500 flex-shrink-0" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-tr from-blue-500/20 to-purple-500/20 rounded-3xl blur-2xl" />
            <div className="relative bg-ink-800 border border-ink-600 rounded-3xl p-8 shadow-2xl">
              {/* Abstract UI Representation */}
              <div className="flex items-center justify-between mb-8 pb-4 border-b border-ink-600">
                <div className="flex items-center gap-3">
                  <div className="w-3 h-3 rounded-full bg-red-500" />
                  <div className="w-3 h-3 rounded-full bg-yellow-500" />
                  <div className="w-3 h-3 rounded-full bg-green-500" />
                </div>
                <div className="text-xs text-slate-500 font-mono">sentinel://impact-analysis</div>
              </div>
              <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="flex items-center gap-4 p-4 rounded-xl bg-ink-900 border border-ink-600">
                    <div className="w-10 h-10 rounded-lg bg-blue-500/20 flex items-center justify-center">
                      <Activity size={18} className="text-blue-400" />
                    </div>
                    <div className="flex-1">
                      <div className="h-2 w-24 bg-slate-700 rounded mb-2" />
                      <div className="h-2 w-16 bg-slate-800 rounded" />
                    </div>
                    <div className="text-sm font-mono text-red-400">sev 0.8{i}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* --- CTA SECTION --- */}
      <section className="relative px-6 py-24 border-t border-ink-600 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-blue-500/5 to-transparent pointer-events-none" />
        <div className="max-w-4xl mx-auto text-center relative z-10">
          <h2 className="text-4xl md:text-5xl font-bold text-white tracking-tight mb-6">Ready to secure your supply chain?</h2>
          <p className="text-xl text-slate-400 mb-10">Join the forward-thinking companies using Sentinel to predict and prevent disruptions.</p>
          <Link to="/login" className="btn text-lg px-10 py-4 shadow-xl shadow-blue-500/20 hover:scale-105 transition-transform inline-flex items-center gap-2">
            Get Started for Free <ArrowRight size={20} />
          </Link>
        </div>
      </section>

      {/* --- FOOTER --- */}
      <footer className="border-t border-ink-600 bg-ink-900 py-12 px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2">
            <ShieldCheck className="text-blue-500" size={20} />
            <span className="text-white font-semibold">Sentinel Control Tower</span>
          </div>
          <div className="flex gap-8 text-sm text-slate-500">
            <a href="#" className="hover:text-slate-300 transition-colors">Privacy Policy</a>
            <a href="#" className="hover:text-slate-300 transition-colors">Terms of Service</a>
            <a href="#" className="hover:text-slate-300 transition-colors">Contact</a>
          </div>
          <div className="text-xs text-slate-600">
            © {new Date().getFullYear()} Sentinel AI. All rights reserved.
          </div>
        </div>
      </footer>

      {/* Simple CSS for animations (add to your global CSS if not using Tailwind config for these) */}
      <style>{`
        @keyframes fadeInUp {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in-up {
          animation: fadeInUp 0.8s ease-out forwards;
          opacity: 0;
        }
        .animation-delay-100 { animation-delay: 100ms; }
        .animation-delay-200 { animation-delay: 200ms; }
        .animation-delay-300 { animation-delay: 300ms; }
      `}</style>
    </div>
  )
}