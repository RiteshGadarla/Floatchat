import { Navigation } from "@/components/navigation"
import { HeroSection } from "@/components/hero-section"
import { JoinOdysseySection } from "@/components/join-odyssey-section"
import { StatsSection } from "@/components/stats-section"
import { ExpeditionSection } from "@/components/expedition-section"
import { ExplorerSection } from "@/components/explorer-section"
import { MissionSection } from "@/components/mission-section"
import { WhyItMattersSection } from "@/components/why-it-matters-section"

export default function HomePage() {
  return (
    <div className="min-h-screen  text-white overflow-x-hidden">
      <Navigation />
      <HeroSection />
      <JoinOdysseySection />
      {/* <div className="h-40 w-full bg-gradient-to-b from-blue-500 via-purple-500 to-pink-500"></div> */}

      <StatsSection />
      <ExpeditionSection />
      <ExplorerSection />
      <MissionSection />
      <WhyItMattersSection />
    </div>
  )
}
