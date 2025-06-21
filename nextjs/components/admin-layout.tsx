"use client"

import type React from "react"

import { useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import {
  LayoutDashboard,
  Settings,
  Activity,
  GitBranch,
  Database,
  MapPin,
  FileText,
  Users,
  BarChart3,
  Cog,
  Menu,
  Server,
} from "lucide-react"

const menuItems = [
  {
    title: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
    description: "Panoramica generale del sistema",
  },
  {
    title: "Status",
    href: "/status",
    icon: Activity,
    description: "Stato dei servizi e connessioni",
  },
  {
    title: "Config",
    href: "/config",
    icon: Settings,
    description: "Configurazione del sistema",
  },
  {
    title: "Lineage",
    href: "/lineage",
    icon: GitBranch,
    description: "Tracciabilità dei metadati",
  },
  {
    title: "Connections",
    href: "/connections",
    icon: Database,
    description: "Gestione connessioni SAP",
  },
  {
    title: "Mappings",
    href: "/mappings",
    icon: MapPin,
    description: "Mappature dei metadati",
  },
  {
    title: "Logs",
    href: "/logs",
    icon: FileText,
    description: "Log di sistema e audit",
  },
  {
    title: "Users",
    href: "/users",
    icon: Users,
    description: "Gestione utenti e permessi",
  },
  {
    title: "Reports",
    href: "/reports",
    icon: BarChart3,
    description: "Report e analytics",
  },
  {
    title: "Settings",
    href: "/settings",
    icon: Cog,
    description: "Impostazioni generali",
  },
]

interface AdminLayoutProps {
  children: React.ReactNode
}

export function AdminLayout({ children }: AdminLayoutProps) {
  const pathname = usePathname()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const SidebarContent = () => (
    <div className="flex h-full flex-col">
      <div className="flex h-14 items-center border-b px-4">
        <div className="flex items-center gap-2">
          <Server className="h-6 w-6 text-primary" />
          <span className="font-semibold">SAP PO Admin</span>
        </div>
      </div>
      <ScrollArea className="flex-1 px-3">
        <div className="space-y-2 py-4">
          {menuItems.map((item) => {
            const Icon = item.icon
            const isActive = pathname === item.href
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setSidebarOpen(false)}
                className={cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors hover:bg-accent hover:text-accent-foreground",
                  isActive ? "bg-accent text-accent-foreground" : "text-muted-foreground",
                )}
              >
                <Icon className="h-4 w-4" />
                <div className="flex flex-col">
                  <span className="font-medium">{item.title}</span>
                  <span className="text-xs text-muted-foreground">{item.description}</span>
                </div>
              </Link>
            )
          })}
        </div>
      </ScrollArea>
    </div>
  )

  return (
    <div className="flex h-screen">
      {/* Desktop Sidebar */}
      <div className="hidden w-64 border-r bg-background lg:block">
        <SidebarContent />
      </div>

      {/* Mobile Sidebar */}
      <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
        <SheetTrigger asChild>
          <Button variant="ghost" size="icon" className="lg:hidden fixed top-4 left-4 z-40">
            <Menu className="h-6 w-6" />
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-64 p-0">
          <SidebarContent />
        </SheetContent>
      </Sheet>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">{children}</div>
    </div>
  )
}
