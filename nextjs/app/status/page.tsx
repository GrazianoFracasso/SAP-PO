"use client"

import { useMemo, useState } from "react"
import { AdminLayout } from "@/components/admin-layout"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { AlertTriangle, CheckCircle, Clock3, Loader2, Play, RefreshCw, Search, XCircle } from "lucide-react"

type ActionType = "refresh" | "status" | "complete"

type BackendStatus = {
  status?: string
  percent_complete?: number
  processed?: number
  total?: number
  message?: string
  [key: string]: unknown
}

type Entity = {
  key: string
  label: string
  description: string
}

type EntityState = {
  loadingAction?: ActionType
  lastAction?: ActionType
  lastChecked?: string
  response?: BackendStatus
  error?: string
  history: Array<{
    action: ActionType
    status: string
    percent: number
    time: string
  }>
}

const entities: Entity[] = [
  {
    key: "communication_channels",
    label: "Communication Channels",
    description: "Canali di comunicazione SAP PO",
  },
  {
    key: "integration_configurations",
    label: "Integration Configurations",
    description: "Configurazioni integrate end-to-end",
  },
  {
    key: "value_mappings",
    label: "Value Mappings",
    description: "Mapping valori e domini applicativi",
  },
  {
    key: "sender_agreements",
    label: "Sender Agreements",
    description: "Accordi lato mittente",
  },
  {
    key: "receiver_agreements",
    label: "Receiver Agreements",
    description: "Accordi lato ricevente",
  },
]

const initialState = entities.reduce<Record<string, EntityState>>((acc, entity) => {
  acc[entity.key] = { history: [] }
  return acc
}, {})

function getPercent(response?: BackendStatus) {
  if (!response) return 0
  if (typeof response.percent_complete === "number") return Math.max(0, Math.min(100, response.percent_complete))
  if (typeof response.processed === "number" && typeof response.total === "number" && response.total > 0) {
    return Math.round((response.processed / response.total) * 100)
  }
  return response.status === "completed" ? 100 : 0
}

function formatStatus(status?: string) {
  if (!status) return "Non controllato"
  if (status === "started") return "Avviato"
  if (status === "running") return "In corso"
  if (status === "completed") return "Completato"
  if (status === "error") return "Errore"
  return status
}

function statusVariant(status?: string) {
  if (status === "completed") return "bg-green-100 text-green-800 hover:bg-green-100"
  if (status === "running" || status === "started") return "bg-blue-100 text-blue-800 hover:bg-blue-100"
  if (status === "error") return ""
  return "bg-slate-100 text-slate-700 hover:bg-slate-100"
}

function StatusIcon({ status, loading }: { status?: string; loading?: boolean }) {
  if (loading) return <Loader2 className="h-4 w-4 animate-spin text-blue-600" />
  if (status === "completed") return <CheckCircle className="h-4 w-4 text-green-600" />
  if (status === "running" || status === "started") return <Clock3 className="h-4 w-4 text-blue-600" />
  if (status === "error") return <XCircle className="h-4 w-4 text-red-600" />
  return <AlertTriangle className="h-4 w-4 text-slate-500" />
}

export default function StatusPage() {
  const [states, setStates] = useState<Record<string, EntityState>>(initialState)
  const [globalAction, setGlobalAction] = useState<ActionType | undefined>()

  const summary = useMemo(() => {
    const values = Object.values(states)
    return {
      completed: values.filter((item) => item.response?.status === "completed").length,
      running: values.filter((item) => item.response?.status === "running" || item.response?.status === "started").length,
      errors: values.filter((item) => item.error || item.response?.status === "error").length,
      checked: values.filter((item) => item.lastChecked).length,
    }
  }, [states])

  async function callEndpoint(entity: Entity, action: ActionType) {
    setStates((current) => ({
      ...current,
      [entity.key]: {
        ...current[entity.key],
        loadingAction: action,
        lastAction: action,
        error: undefined,
      },
    }))

    try {
      const response = await fetch(`/api/backend/extract/full/${entity.key}/${action}`, {
        method: "GET",
        cache: "no-store",
      })
      const payload = (await response.json()) as BackendStatus

      if (!response.ok) {
        throw new Error(payload.message || `HTTP ${response.status}`)
      }

      const percent = getPercent(payload)
      const now = new Date().toLocaleTimeString("it-IT", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      })

      setStates((current) => ({
        ...current,
        [entity.key]: {
          ...current[entity.key],
          loadingAction: undefined,
          response: payload,
          lastChecked: now,
          history: [
            { action, status: payload.status || "unknown", percent, time: now },
            ...current[entity.key].history,
          ].slice(0, 6),
        },
      }))
    } catch (error) {
      const message = error instanceof Error ? error.message : "Errore sconosciuto"
      const now = new Date().toLocaleTimeString("it-IT", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      })

      setStates((current) => ({
        ...current,
        [entity.key]: {
          ...current[entity.key],
          loadingAction: undefined,
          error: message,
          response: { status: "error", message },
          lastChecked: now,
          history: [{ action, status: "error", percent: 0, time: now }, ...current[entity.key].history].slice(0, 6),
        },
      }))
    }
  }

  async function callAll(action: ActionType) {
    setGlobalAction(action)
    await Promise.all(entities.map((entity) => callEndpoint(entity, action)))
    setGlobalAction(undefined)
  }

  return (
    <AdminLayout>
      <main className="space-y-6 p-6">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h1 className="text-3xl font-bold">Refresh metadati</h1>
            <p className="text-muted-foreground">Avvio estrazioni backend e controllo avanzamento per ogni entita.</p>
          </div>
          <div className="flex flex-wrap gap-2">
            <Button variant="outline" onClick={() => callAll("status")} disabled={Boolean(globalAction)}>
              {globalAction === "status" ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Search className="mr-2 h-4 w-4" />}
              Stato
            </Button>
            <Button variant="outline" onClick={() => callAll("complete")} disabled={Boolean(globalAction)}>
              {globalAction === "complete" ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <RefreshCw className="mr-2 h-4 w-4" />}
              Complete
            </Button>
            <Button onClick={() => callAll("refresh")} disabled={Boolean(globalAction)}>
              {globalAction === "refresh" ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Play className="mr-2 h-4 w-4" />}
              Refresh completo
            </Button>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-4">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Controllate</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{summary.checked}/{entities.length}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">In corso</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{summary.running}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Completate</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{summary.completed}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Errori</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{summary.errors}</div>
            </CardContent>
          </Card>
        </div>

        <div className="grid gap-4 xl:grid-cols-2">
          {entities.map((entity) => {
            const state = states[entity.key]
            const response = state.response
            const percent = getPercent(response)
            const isLoading = Boolean(state.loadingAction)

            return (
              <Card key={entity.key}>
                <CardHeader className="space-y-3">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <CardTitle className="flex items-center gap-2 text-lg">
                        <StatusIcon status={response?.status} loading={isLoading} />
                        {entity.label}
                      </CardTitle>
                      <CardDescription>{entity.description}</CardDescription>
                    </div>
                    <Badge variant={response?.status === "error" ? "destructive" : "secondary"} className={statusVariant(response?.status)}>
                      {formatStatus(response?.status)}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-5">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Avanzamento</span>
                      <span className="font-medium">{percent}%</span>
                    </div>
                    <Progress value={percent} className="h-2" />
                    <div className="flex items-center justify-between text-xs text-muted-foreground">
                      <span>
                        Processati {typeof response?.processed === "number" ? response.processed : "-"} /{" "}
                        {typeof response?.total === "number" ? response.total : "-"}
                      </span>
                      <span>Ultimo check: {state.lastChecked || "-"}</span>
                    </div>
                  </div>

                  {state.error ? (
                    <div className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800">{state.error}</div>
                  ) : null}

                  <div className="flex flex-wrap gap-2">
                    <Button size="sm" onClick={() => callEndpoint(entity, "refresh")} disabled={isLoading || Boolean(globalAction)}>
                      {state.loadingAction === "refresh" ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Play className="mr-2 h-4 w-4" />}
                      Refresh
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => callEndpoint(entity, "status")} disabled={isLoading || Boolean(globalAction)}>
                      {state.loadingAction === "status" ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Search className="mr-2 h-4 w-4" />}
                      Status
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => callEndpoint(entity, "complete")} disabled={isLoading || Boolean(globalAction)}>
                      {state.loadingAction === "complete" ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <RefreshCw className="mr-2 h-4 w-4" />}
                      Complete
                    </Button>
                  </div>

                  <div className="space-y-2">
                    <div className="text-sm font-medium">Andamento recente</div>
                    {state.history.length ? (
                      <div className="space-y-2">
                        {state.history.map((item, index) => (
                          <div key={`${item.time}-${index}`} className="flex items-center justify-between rounded-md border px-3 py-2 text-sm">
                            <span className="font-medium">{item.action}</span>
                            <span className="text-muted-foreground">{formatStatus(item.status)}</span>
                            <span className="tabular-nums">{item.percent}%</span>
                            <span className="text-muted-foreground">{item.time}</span>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="rounded-md border border-dashed px-3 py-3 text-sm text-muted-foreground">Nessuna chiamata eseguita.</div>
                    )}
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>
      </main>
    </AdminLayout>
  )
}
