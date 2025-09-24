"use client"

import { useEffect, useRef, useState } from "react"

export function StatsSection() {
  const sectionRef = useRef<HTMLElement>(null)
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(true)
          }
        })
      },
      { threshold: 0.3 },
    )

    if (sectionRef.current) {
      observer.observe(sectionRef.current)
    }

    return () => observer.disconnect()
  }, [])

  return (
    <section ref={sectionRef} className="py-20 px-4 relative">
      <div className="absolute inset-0">
        <img src="/stats.png" alt="Underwater ocean scene" className="w-full h-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-b from-slate-950/20 via-slate-950/40 to-slate-950/80"></div>
      </div>
      <div className="max-w-7xl mx-auto">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left - Stats */}
          <div
            className={`space-y-8 ${isVisible ? "animate-in fade-in slide-in-from-left-8 duration-1000" : "opacity-0"}`}
          >
            <div className="space-y-4">
              <div className="text-sm text-cyan-400 font-semibold tracking-wider">OCEAN FACTS</div>
              <h2 className="text-5xl md:text-6xl font-bold text-white leading-tight text-balance">
                ACCESS{" "}
                <span className="text-transparent bg-gradient-to-r from-cyan-400 to-teal-400 bg-clip-text">FASTER</span> 
                <br />A{" "}
                <span className="text-transparent bg-gradient-to-r from-cyan-400 to-teal-400 bg-clip-text">
                  UNIFIED
                </span> <br />
                <span className="text-transparent bg-gradient-to-r from-cyan-400 to-teal-400 bg-clip-text">
                  OCEAN
                </span>{" "}
                 DATASET
              </h2>
              <p className="text-white/70 text-lg leading-relaxed max-w-md">
                FloatChat's mission is to democratize access to vast, complex oceanographic data, making it understandable and accessible to everyone.
              </p>
            </div>

            <div className="space-y-6">
              <p className="text-white/80 leading-relaxed">
                From querying specific salinity profiles to comparing BGC parameters across different regions, our AI-powered system simplifies the exploration of ARGO float data.
              </p>
              <p className="text-white/80 leading-relaxed">
                Start your data discovery journey by asking simple questions and visualizing meaningful insights with our interactive dashboards.
              </p>
            </div>
          </div>

          {/* Right - Image */}
          <div
            className={`relative ${isVisible ? "animate-in fade-in slide-in-from-right-8 duration-1000 delay-300" : "opacity-0"}`}
          >
            <div className="relative rounded-2xl overflow-hidden">
              <img
                src="/bioluminescent-jellyfish-floating-in-deep-ocean-wa.jpg"
                alt="Bioluminescent jellyfish"
                className="w-full h-[500px] object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-950/40 via-transparent to-transparent"></div>
            </div>

            {/* Floating stats */}
            <div className="absolute -top-4 -right-4 bg-slate-900/90 backdrop-blur-sm rounded-xl p-4 border border-cyan-500/20">
              <div className="text-2xl font-bold text-cyan-400">1.5M+</div>
              <div className="text-sm text-white/70">Profiles</div>
            </div>

            <div className="absolute -bottom-4 -left-4 bg-slate-900/90 backdrop-blur-sm rounded-xl p-4 border border-teal-500/20">
              <div className="text-2xl font-bold text-teal-400">4000+</div>
              <div className="text-sm text-white/70">Floats</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
