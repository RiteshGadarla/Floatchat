"use client"

import type React from "react"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { MessageCircle, Database, BarChart3, Map, Download, Send, Waves, FileText, Loader2 } from "lucide-react"

interface ChatMessage {
  role: "user" | "assistant"
  content: string
  sqlQuery?: string
  summary?: string
  dataPreview?: any[]
  totalEntries?: number
  visualizations?: string[]
  mapHtml?: string
}

export default function FloatChatApp() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: ChatMessage = {
      role: "user",
      content: input.trim(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    // Simulate API call
    setTimeout(() => {
      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: "Here are your query results:",
        sqlQuery: `SELECT latitude, longitude, temperature, salinity, depth 
FROM oceanographic_data 
WHERE temperature > 15 
AND depth < 1000 
ORDER BY temperature DESC 
LIMIT 100;`,
        summary:
          "Found 100 oceanographic measurements with temperatures above 15°C at depths less than 1000m. The data shows a clear correlation between temperature and depth, with warmer waters typically found in shallower regions. Average temperature: 18.5°C, Average depth: 450m.",
        dataPreview: [
          { latitude: 34.0522, longitude: -118.2437, temperature: 22.1, salinity: 34.5, depth: 250 },
          { latitude: 36.7783, longitude: -119.4179, temperature: 21.8, salinity: 34.2, depth: 180 },
          { latitude: 40.7128, longitude: -74.006, temperature: 20.5, salinity: 35.1, depth: 320 },
          { latitude: 25.7617, longitude: -80.1918, temperature: 24.3, salinity: 36.2, depth: 150 },
          { latitude: 32.7767, longitude: -96.797, temperature: 19.2, salinity: 33.8, depth: 480 },
        ],
        totalEntries: 100,
        visualizations: ["temperature_depth_scatter", "salinity_distribution"],
        mapHtml: "<div>Interactive map would be rendered here</div>",
      }

      setMessages((prev) => [...prev, assistantMessage])
      setIsLoading(false)
    }, 2000)
  }

  const downloadCSV = () => {
    // Simulate CSV download
    const csvContent =
      "latitude,longitude,temperature,salinity,depth\n34.0522,-118.2437,22.1,34.5,250\n36.7783,-119.4179,21.8,34.2,180"
    const blob = new Blob([csvContent], { type: "text/csv" })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "oceanographic_data.csv"
    a.click()
    window.URL.revokeObjectURL(url)
  }

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Image */}
      <div className="absolute inset-0 -z-10">
        <img src="/chat_bg.jpg" alt="Underwater ocean scene" className="w-full h-full object-cover" />
        {/* <div className="absolute inset-0 bg-gradient-to-b from-slate-950/20 via-slate-950/40 to-slate-950/80"></div> */}
      </div>
      <div className="min-h-screen  from-background via-accent/5 to-primary/5">
        <div className="container mx-auto px-4 py-8 max-w-6xl">
          {/* Header */}
          <div className="text-center mb-8">
              <div className="flex items-center justify-center gap-3 mb-4">
                <h1 className="text-5xl font-extrabold from-blue-300 to-cyan-500 bg-clip-text text-transparent">
                  <div className="flex items-center space-x-4">
                    <img 
                      src="/nav.png" 
                      alt="Logo" 
                      className="w-12 h-12 object-contain"
                    />
                    <span className="text-white">
                      FLOAT CHAT
                    </span>
                  </div>
                </h1>
              </div>
            <p className="text-white text-lg">
              Ocean Data Exploration - Query the oceanographic database using natural language
            </p>
          </div>

          {/* Chat Interface */}
          <Card className="border-primary/20 shadow-lg">
            <div className="p-6">
              {/* Messages */}
              <ScrollArea className="h-[600px] mb-6">
                <div className="space-y-6">
                  {messages.length === 0 && (
                    <div className="text-center py-12">
                      <MessageCircle className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                      <p className="text-muted-foreground">
                        Start exploring ocean data by asking questions in natural language
                      </p>
                      <div className="mt-4 flex flex-wrap gap-2 justify-center">
                        <Badge variant="outline">Temperature trends</Badge>
                        <Badge variant="outline">Salinity levels</Badge>
                        <Badge variant="outline">Deep water analysis</Badge>
                      </div>
                    </div>
                  )}

                  {messages.map((message, index) => (
                    <div key={index} className="space-y-4">
                      {/* User Message */}
                      {message.role === "user" && (
                        <div className="flex justify-end">
                          <div className="bg-primary text-primary-foreground rounded-lg px-4 py-2 max-w-md">
                            {message.content}
                          </div>
                        </div>
                      )}

                      {/* Assistant Message */}
                      {message.role === "assistant" && (
                        <div className="space-y-4">
                          <div className="flex justify-start">
                            <div className="bg-muted rounded-lg px-4 py-2 max-w-md">{message.content}</div>
                          </div>

                          {/* SQL Query */}
                          {message.sqlQuery && (
                            <Card className="bg-card/50">
                              <div className="p-4">
                                <div className="flex items-center gap-2 mb-3">
                                  <Database className="h-4 w-4 text-primary" />
                                  <h4 className="font-semibold">Generated SQL Query</h4>
                                </div>
                                <pre className="bg-muted/50 p-3 rounded text-sm overflow-x-auto">
                                  <code>{message.sqlQuery}</code>
                                </pre>
                              </div>
                            </Card>
                          )}

                          {/* Data Preview */}
                          {message.dataPreview && (
                            <Card className="bg-card/50">
                              <div className="p-4">
                                <div className="flex items-center justify-between mb-3">
                                  <div className="flex items-center gap-2">
                                    <FileText className="h-4 w-4 text-primary" />
                                    <h4 className="font-semibold">Extracted Data Preview</h4>
                                  </div>
                                  <Button
                                    size="sm"
                                    variant="outline"
                                    onClick={downloadCSV}
                                    className="gap-2 bg-transparent"
                                  >
                                    <Download className="h-4 w-4" />
                                    Download CSV
                                  </Button>
                                </div>

                                <div className="overflow-x-auto">
                                  <table className="w-full text-sm">
                                    <thead>
                                      <tr className="border-b">
                                        <th className="text-left p-2">Latitude</th>
                                        <th className="text-left p-2">Longitude</th>
                                        <th className="text-left p-2">Temperature (°C)</th>
                                        <th className="text-left p-2">Salinity</th>
                                        <th className="text-left p-2">Depth (m)</th>
                                      </tr>
                                    </thead>
                                    <tbody>
                                      {message.dataPreview.map((row, i) => (
                                        <tr key={i} className="border-b">
                                          <td className="p-2">{row.latitude}</td>
                                          <td className="p-2">{row.longitude}</td>
                                          <td className="p-2">{row.temperature}</td>
                                          <td className="p-2">{row.salinity}</td>
                                          <td className="p-2">{row.depth}</td>
                                        </tr>
                                      ))}
                                    </tbody>
                                  </table>
                                </div>

                                {message.totalEntries && (
                                  <p className="text-sm text-muted-foreground mt-3">
                                    <strong>Total Entries:</strong> {message.totalEntries}
                                  </p>
                                )}
                              </div>
                            </Card>
                          )}

                          {/* Summary */}
                          {message.summary && (
                            <Card className="bg-card/50">
                              <div className="p-4">
                                <div className="flex items-center gap-2 mb-3">
                                  <FileText className="h-4 w-4 text-primary" />
                                  <h4 className="font-semibold">📌 Summary</h4>
                                </div>
                                <p className="text-sm leading-relaxed">{message.summary}</p>
                              </div>
                            </Card>
                          )}

                          {/* Visualizations */}
                          {message.visualizations && (
                            <Card className="bg-card/50">
                              <div className="p-4">
                                <div className="flex items-center gap-2 mb-3">
                                  <BarChart3 className="h-4 w-4 text-primary" />
                                  <h4 className="font-semibold">📊 Visualization</h4>
                                </div>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                  {message.visualizations.map((viz, i) => (
                                    <div key={i} className="bg-muted/30 rounded-lg p-4 text-center">
                                      <div className="h-32 bg-gradient-to-br from-primary/20 to-chart-2/20 rounded mb-2 flex items-center justify-center">
                                        <BarChart3 className="h-8 w-8 text-primary/60" />
                                      </div>
                                      <p className="text-sm font-medium">{viz.replace(/_/g, " ").toUpperCase()}</p>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            </Card>
                          )}

                          {/* Map */}
                          {message.mapHtml && (
                            <Card className="bg-card/50">
                              <div className="p-4">
                                <div className="flex items-center gap-2 mb-3">
                                  <Map className="h-4 w-4 text-primary" />
                                  <h4 className="font-semibold">🗺️ Map Preview</h4>
                                </div>
                                <div className="bg-muted/30 rounded-lg h-64 flex items-center justify-center">
                                  <div className="text-center">
                                    <Map className="h-12 w-12 text-primary/60 mx-auto mb-2" />
                                    <p className="text-sm text-muted-foreground">
                                      Interactive map would be displayed here
                                    </p>
                                  </div>
                                </div>
                              </div>
                            </Card>
                          )}
                        </div>
                      )}
                    </div>
                  ))}

                  {/* Loading State */}
                  {isLoading && (
                    <div className="flex justify-start">
                      <div className="bg-muted rounded-lg px-4 py-2 flex items-center gap-2">
                        <Loader2 className="h-4 w-4 animate-spin" />
                        <span className="text-sm">⏳ Generating SQL and extracting data...</span>
                      </div>
                    </div>
                  )}
                </div>
              </ScrollArea>

              <Separator className="mb-4" />

              {/* Input Form */}
              <form onSubmit={handleSubmit} className="flex gap-2">
                <Input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="🔍 Enter your query... (e.g., 'Show me temperature data from the Pacific Ocean')"
                  className="flex-1"
                  disabled={isLoading}
                />
                <Button type="submit" disabled={isLoading || !input.trim()}>
                  <Send className="h-4 w-4" />
                </Button>
              </form>
            </div>
          </Card>
        </div>
      </div>
    </section>
  )
}
