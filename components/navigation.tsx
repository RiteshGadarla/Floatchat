"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Menu, X } from "lucide-react"

export function Navigation() {
  const [isScrolled, setIsScrolled] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50)
    }
    window.addEventListener("scroll", handleScroll)

    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 lg:px-12 transition-all duration-300 ${
         "bg-transparent"
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-center">
        {/* Main navigation container with frosted glass effect */}
        <div className={`
          relative flex items-center h-16 px-4 py-2 rounded-full 
          bg-white/10 backdrop-blur-md border border-white/20
          transition-all duration-300
        `}>
          {/* Logo */}
          <div className="flex items-center space-x-2 mr-4">
            {/* Replace with your actual logo SVG/image */}
            <span className="text-xl font-bold text-white uppercase">
              FLOAT CHAT<br/>
            </span>
          </div>

          {/* Desktop Navigation Links */}
          <div className="hidden md:flex items-center space-x-6">
            <a href="#" className="text-white/80 hover:text-white transition-colors text-sm font-light">
              EXPLORE
            </a>
            <a href="#" className="text-white/80 hover:text-white transition-colors text-sm font-light">
              EXPEDETIONS
            </a>
            <a href="#" className="text-white/80 hover:text-white transition-colors text-sm font-light">
              RESEARCH
            </a>
            <a href="#" className="text-white/80 hover:text-white transition-colors text-sm font-light">
              DISCOVERIES
            </a>
            <a href="#" className="text-white/80 hover:text-white transition-colors text-sm font-light">
              ABOUT US
            </a>
          </div>

          {/* CTA Buttons - Segmented style */}
          <div className="hidden md:flex items-center space-x-2 ml-4">
            <Button className="bg-white/10 text-white px-6 py-2 rounded-full border border-white/20 hover:bg-white/20 transition-all text-sm">
              LET'S CONNECT
            </Button>

          </div>

          {/* Mobile menu button */}
          <button 
            className="md:hidden text-white" 
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isMobileMenuOpen && (
        <div className="md:hidden bg-slate-950/95 backdrop-blur-md rounded-lg mx-4 mt-2 p-4 animate-in slide-in-from-top-2">
          <div className="flex flex-col space-y-4">
            <a href="#" className="text-white/80 hover:text-white transition-colors text-sm">ABOUT</a>
            <a href="#" className="text-white/80 hover:text-white transition-colors text-sm">GET INVOLVED</a>
            <a href="#" className="text-white/80 hover:text-white transition-colors text-sm">SCIENCE NETWORK</a>
            <a href="#" className="text-white/80 hover:text-white transition-colors text-sm">DISCOVERIES</a>
            <a href="#" className="text-white/80 hover:text-white transition-colors text-sm">NEWS & EVENTS</a>
            <Button className="bg-white/10 text-white px-6 py-2 rounded-full mt-4 text-sm">
              LET'S CONNECT
            </Button>
            <Button className="bg-white/20 text-white px-6 py-2 rounded-full text-sm">
              MENU
            </Button>
          </div>
        </div>
      )}
    </nav>
  )
}