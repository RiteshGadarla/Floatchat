"use client"

import { useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { ArrowRight } from "lucide-react"

export function ExpeditionSection() {
  const sectionRef = useRef<HTMLElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("animate-in", "fade-in", "slide-in-from-bottom-8")
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
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4 text-balance">
            <span className="text-transparent bg-gradient-to-r from-cyan-400 to-teal-400 bg-clip-text">
              UNLOCK OCEAN INSIGHTS
            </span>
          </h2>
          <p className="text-xl text-white/70 max-w-2xl mx-auto text-balance">YOUR CONVERSATIONAL ARGO CHATBOT</p>
        </div>
 
        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-12 items-center mb-16">
          {/* Left - Image */}
          <div className="relative">
            <div className="relative rounded-2xl overflow-hidden group">
              <img
                src="/underwater-research-expedition-with-divers-explori.jpg"
                alt="Ocean expedition"
                className="w-full h-[400px] object-cover transition-transform duration-700 group-hover:scale-105"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-950/60 via-transparent to-transparent"></div>
            </div>
          </div>

          {/* Right - Content */}
          <div className="space-y-6">
            <p className="text-white/80 text-lg leading-relaxed">
              Float Chat is your personal guide to the ocean's secrets. Ask questions in plain English and receive instant visualizations and insights from the vast ARGO dataset. Get accurate answers on salinity, temperature, and BGC parameters without complex tools or data science skills.
            </p>
            <p className="text-white/70 leading-relaxed">JOIN THE DISCOVERY.</p>

            <Button className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white px-6 py-3 rounded-full font-semibold transition-all duration-300 hover:scale-105 flex items-center gap-2">
              START CONVERSING
              <ArrowRight size={18} />
            </Button>
          </div>
        </div>

        {/* Bottom Cards */}
        <div className="grid md:grid-cols-3 gap-6">
          {[
            {
              title: "Salinity & Temperature Profiles",
              description: "Discover the mysteries of the deep ocean with our advanced submersibles",
              image: "deep sea exploration with submersible and bioluminescent creatures",
            },
            {
              title: "BGC Parameter Analysis",
              description: "Compare critical BGC parameters like chlorophyll, dissolved oxygen, and nitrate across different regions and timeframes.",
              image: "colorful coral reef with tropical fish and marine life",
            },
            {
              title: "ARGO Float Trajectories",
              description: "Visualize the mapped trajectories of individual ARGO floats, exploring their paths and historical data.",
              image: "diverse marine life including whales, dolphins and exotic fish",
            },
          ].map((card, index) => (
            <div key={index} className="group cursor-pointer">
              <div className="relative rounded-xl overflow-hidden mb-4">
                <img
                  src={`/abstract-geometric-shapes.png?height=200&width=300&query=${card.image}`}
                  alt={card.title}
                  className="w-full h-48 object-cover transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent"></div>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2 group-hover:text-cyan-400 transition-colors">
                {card.title}
              </h3>
              <p className="text-white/70 text-sm leading-relaxed">{card.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
