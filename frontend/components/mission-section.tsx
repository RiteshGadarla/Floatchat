"use client"

import { useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"

export function MissionSection() {
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
      {/* Background */}
      <div className="absolute inset-0">
        <img
          src="/underwater-scene-with-bioluminescent-organisms-and.jpg"
          alt="Deep ocean background"
          className="w-full h-full object-cover opacity-30"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-slate-950/90 via-slate-950/70 to-slate-950/90"></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto grid lg:grid-cols-2 gap-12 items-center">
        {/* Left - Image */}
        <div className="relative">
          <div className="relative rounded-2xl overflow-hidden">
            <img src="/underwater-diver-with-advanced-equipment-exploring.jpg" alt="Deep sea mission" className="w-full h-[600px] object-cover" />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-950/60 via-transparent to-transparent"></div>

            {/* Mission stats */}
            <div className="absolute top-6 right-6 space-y-3">
              <div className="bg-slate-900/90 backdrop-blur-sm rounded-lg p-3 border border-yellow-500/20">
                <div className="text-lg font-bold text-yellow-400">27/7</div>
                <div className="text-xs text-white/70">Data Access</div>
              </div>
              <div className="bg-slate-900/90 backdrop-blur-sm rounded-lg p-3 border border-green-500/20">
                <div className="text-lg font-bold text-green-400">26</div>
                <div className="text-xs text-white/70">Participating Countries</div>
              </div>
            </div>
          </div>
        </div>

        {/* Right - Content */}
        <div className="space-y-8">
          <div>
            <h2 className="text-5xl md:text-6xl font-bold mb-6 text-balance">
              <span className="text-white">CHAT TO</span>
              <br />
              <span className="text-transparent bg-gradient-to-r from-yellow-400 via-orange-500 to-red-500 bg-clip-text">
                EXPLORE
              </span>
            </h2>
            <p className="text-lg text-white/80 leading-relaxed">
              Float Chat is designed to help you make informed decisions. By conversing with vast ARGO datasets, you gain a deeper understanding of oceanographic parameters and their impact on our planet.
            </p>
          </div>

          <div className="space-y-6">
            <div className="flex items-start gap-4">
              <div className="w-3 h-3 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full mt-2 flex-shrink-0"></div>
              <div>
                <h3 className="text-white font-semibold mb-2">QUERY COMPLEX DATA</h3>
                <p className="text-white/70 text-sm leading-relaxed">
                  Ask questions in plain language to retrieve specific profiles, compare parameters, or find data from a given location and time.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-3 h-3 bg-gradient-to-r from-orange-500 to-red-500 rounded-full mt-2 flex-shrink-0"></div>
              <div>
                <h3 className="text-white font-semibold mb-2">VISUALIZE YOUR INSIGHTS</h3>
                <p className="text-white/70 text-sm leading-relaxed">
                 Automatically generate interactive maps, charts, and plots to see your data and understand trends at a glance.
                </p>
              </div>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4">
            <Button className="bg-gradient-to-r from-yellow-500 to-orange-600 hover:from-yellow-600 hover:to-orange-700 text-white px-8 py-3 rounded-full font-semibold transition-all duration-300 hover:scale-105">
              START CHATTING
            </Button>
            <Button
              variant="outline"
              className="border-white/30 text-white hover:bg-white/10 px-8 py-3 rounded-full font-semibold transition-all duration-300 bg-transparent"
            >
              VIEW EXAMPLES
            </Button>
          </div>
        </div>
      </div>
    </section>
  )
}
