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
      <StatsSection />
      <ExpeditionSection />
      <ExplorerSection />
      <MissionSection />
      <WhyItMattersSection />
    </div>
  )
}
