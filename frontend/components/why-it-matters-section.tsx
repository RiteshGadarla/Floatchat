"use client"

import { useEffect, useRef } from "react"

// We've removed external imports for Button and Play.
// They are now defined within this single file to prevent errors.

// The "Button" component is now a self-contained functional component.
const Button = ({ children, className, variant, ...props }) => {
  const baseClasses = "px-8 py-3 rounded-full text-lg font-semibold transition-all duration-300 hover:scale-105"
  const variantClasses = {
    default: "bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white hover:shadow-lg hover:shadow-cyan-500/25",
    outline: "border-white/30 text-white hover:bg-white/10 bg-transparent"
  }
  const mergedClasses = `${baseClasses} ${variantClasses[variant] || variantClasses.default} ${className}`

  return (
    <button className={mergedClasses} {...props}>
      {children}
    </button>
  )
}

// Replaced the external Play icon with an inline SVG.
const PlayIcon = ({ size = 24, className = "" }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
  >
    <polygon points="5 3 19 12 5 21 5 3"></polygon>
  </svg>
);


export function WhyItMattersSection() {
  const sectionRef = useRef(null)

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
    <section 
      ref={sectionRef} 
      className="py-20 px-4 relative overflow-hidden bg-cover bg-center"
      style={{ backgroundImage: "url('/underwater-coral-reef-ecosystem-with-diverse-marin1.jpg')" }}
    >
      {/* Overlay to darken the image */}
      <div className="absolute inset-0 bg-slate-950/90"></div>

      {/* Content, now on top of the background image */}
      <div className="relative z-10 max-w-7xl mx-auto">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left - Content and play button */}
          <div className="relative p-8 rounded-2xl bg-slate-900/50 backdrop-blur-md">
            <div className="space-y-6">
              
              <h2 className="text-5xl md:text-6xl font-bold text-white mb-6 text-balance">
                <span className="text-transparent bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text">WHY IT</span>
                <br />
                <span className="text-white">MATTERS</span>
              </h2>
              <p className="text-lg text-white/80 leading-relaxed max-w-lg">
                A new tool for understanding our oceans. FloatChat helps democratize access to vast oceanographic data, enabling smarter decisions for our planet's future.
              </p>
            </div>
            {/* The rest of the content (Climate Insights, Research Acceleration) */}
            <div className="space-y-6 mt-8">
              <div className="bg-slate-900/50 backdrop-blur-sm rounded-lg p-6 border border-cyan-500/20">
                <h3 className="text-xl font-semibold text-cyan-400 mb-3">Climate Insights</h3>
                <p className="text-white/70 leading-relaxed">
                  Analyze how key parameters like temperature and salinity change over time to better understand the ocean's role in climate.
                </p>
              </div>
              <div className="bg-slate-900/50 backdrop-blur-sm rounded-lg p-6 border border-blue-500/20">
                <h3 className="text-xl font-semibold text-blue-400 mb-3">Research Acceleration</h3>
                <p className="text-white/70 leading-relaxed">
                  Empower researchers, students, and policymakers to find the data they need in seconds, not weeks, accelerating scientific discovery.
                </p>
              </div>
            </div>
          </div>
          
          {/* Right - Video/Image */}
          <div className="relative rounded-2xl overflow-hidden group">
            <img
              src="/underwater-documentary-scene-with-marine-biologist.jpg"
              alt="Ocean research documentary"
              className="w-full h-[500px] object-cover transition-transform duration-700 group-hover:scale-105"
            />
            {/* Overlay to create the darker effect */}
            <div className="absolute inset-0 bg-slate-950/40 group-hover:bg-slate-950/20 transition-colors duration-300"></div>

            {/* Play button overlay */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-20 h-20 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center group-hover:bg-white/30 transition-all duration-300 group-hover:scale-110">
                <PlayIcon size={32} className="text-white ml-1" />
              </div>
            </div>

            {/* Duration badge */}
            <div className="absolute bottom-4 right-4 bg-slate-900/90 backdrop-blur-sm rounded-lg px-3 py-1 text-sm text-white">
              4:32
            </div>
          </div>
        </div>

        {/* Bottom CTA */}
        <div className="text-center mt-20 space-y-6">
          <h3 className="text-3xl font-bold text-white text-balance">Ready to Unlock the Ocean's Secrets?</h3>
          <p className="text-white/70 text-lg max-w-2xl mx-auto text-balance">
            Join researchers, data scientists, and policymakers using our AI-powered chatbot to make faster, more informed decisions about our oceans.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a href="http://localhost:8501">
            <Button className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white px-8 py-3 rounded-full text-lg font-semibold transition-all duration-300 hover:scale-105">
              START CHATTING
            </Button>
            </a>
            <Button
              variant="outline"
              className="border-white/30 text-white hover:bg-white/10 px-8 py-3 rounded-full text-lg font-semibold transition-all duration-300 bg-transparent"
            >
              LEARN MORE
            </Button>
          </div>
        </div>
      </div>
    </section>
  )
}
