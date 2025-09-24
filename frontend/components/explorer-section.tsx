"use client"

import { useEffect, useRef } from "react"

export function ExplorerSection() {
  const sectionRef = useRef<HTMLElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("animate-in", "fade-in", "slide-in-from-left-8")
          }
        })
      },
      { threshold: 0.1 },
    )

    if (sectionRef.current) {
      observer.observe(sectionRef.current)
    }

    return () => observer.disconnect()
  }, [])

  return (
    <section ref={sectionRef} className="py-20 px-4 relative">
      <div className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-12 items-center">
        {/* Left - Content */}
        <div className="space-y-8">
          <div>
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6 text-balance">
              <span className="text-transparent bg-gradient-to-r from-cyan-400 to-teal-400 bg-clip-text">
                YOUR AI-POWERED GUIDE:
              </span>
            </h2>
            <p className="text-lg text-white/80 leading-relaxed">
               FloatChat is your AI-powered assistant for oceanographic data discovery. Our system leverages advanced retrieval-augmented generation (RAG) and multimodal large language models (LLMs) to provide instant, meaningful insights from vast datasets.
            </p>
          </div>

          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 bg-cyan-400 rounded-full"></div>
              <span className="text-white/70">Natural language query interface</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 bg-teal-400 rounded-full"></div>
              <span className="text-white/70">Interactive data visualizations</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
              <span className="text-white/70">Seamless data discovery</span>
            </div>
          </div>
        </div>
 
        {/* Right - Image */}
        <div className="relative">
          <div className="relative rounded-2xl overflow-hidden">
            <img
              src="/modern-research-vessel-on-ocean-surface-with-under.jpg"
              alt="OceanXplorer research vessel"
              className="w-full h-[500px] object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-950/40 via-transparent to-transparent"></div>

            {/* Tech overlay */}
            <div className="absolute bottom-6 left-6 bg-slate-900/90 backdrop-blur-sm rounded-lg p-4 border border-cyan-500/20">
              <div className="text-sm text-cyan-400 font-semibold">DEPTH CAPABILITY</div>
              <div className="text-2xl font-bold text-white">6,000m</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
