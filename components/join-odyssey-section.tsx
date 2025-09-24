"use client"

import { Button } from "@/components/ui/button"
import { useEffect, useRef } from "react"

export function JoinOdysseySection() {
  const sectionRef = useRef<HTMLElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("animate-in", "fade-in", "slide-in-from-right-8")
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
    <section ref={sectionRef} className="py-20 px-4 relative overflow-hidden">
            {/* Background Image */}
      <div className="absolute inset-0">
        <img src="/interactArgo.png" alt="Underwater ocean scene" className="w-full h-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-b from-slate-950/20 via-slate-950/40 to-slate-950/80"></div>
      </div>
      {/* Background Image */}
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0 bg-gradient-to-r from-slate-950/90 via-slate-950/70 to-slate-950/90"></div>
      </div>

      <div className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-12 items-center relative z-10"> {/* Added z-10 here */}
        {/* Left Content */}
        <div className="space-y-8">
          <div>
            <h2 className="text-5xl md:text-6xl font-bold mb-6 text-balance">
              <span className="text-transparent bg-gradient-to-r from-cyan-400 to-teal-400 bg-clip-text">INTERACT</span>
              <br />
              <span className="text-white">WITH ARGO DATA</span>
            </h2>
            <p className="text-lg text-white/80 leading-relaxed max-w-lg">
              Float Chat bridges the gap between domain experts, decision-makers, and raw data. Using natural language, you can effortlessly query, visualize, and analyze vast ARGO oceanographic datasets.
            </p>
          </div>

          <Button className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white px-8 py-3 rounded-full text-lg font-semibold transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-cyan-500/25">
            DISCOVER DATA
          </Button>
        </div>

        {/* Right Content - Image */}
        <div className="relative"> 
          <div className="relative rounded-2xl overflow-hidden group">
            <img
              src="/interArgoside.png" // Placeholder for your coral reef image
              alt="Vibrant coral reef with sunlight"
              className="w-full h-[400px] object-cover transition-transform duration-700 group-hover:scale-105"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-950/60 via-transparent to-transparent"></div>

            {/* Floating elements */}
            <div className="absolute top-4 right-4 w-3 h-3 bg-cyan-400 rounded-full animate-pulse"></div>
            <div className="absolute bottom-20 left-6 w-2 h-2 bg-teal-400 rounded-full animate-pulse delay-1000"></div>
            <div className="absolute top-1/3 left-4 w-1 h-1 bg-blue-400 rounded-full animate-pulse delay-500"></div>
          </div>
        </div>
      </div>
    </section>
  )
}