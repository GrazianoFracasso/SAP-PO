"use client"

import { useEffect, useMemo, useRef, useState } from "react"
import {
  AlertTriangle,
  Check,
  ChevronRight,
  Clock3,
  DatabaseZap,
  Loader2,
  Pause,
  Play,
  RefreshCw,
  RotateCcw,
  Server,
  Settings2,
  X,
} from "lucide-react"

type Phase = "idle" | "list" | "object" | "poll"
type StepState = "idle" | "running" | "success" | "error"

type BackendPayload = {
  status?: string
  environment?: string
  percent_complete?: number
  processed?: number
  total?: number
  message?: string
  detail?: string
  [key: string]: unknown
}

type Entity = {
  key: string
  listKey: string
  title: string
  short: string
}

type EntityRuntime = {
  listState: StepState
  objectState: StepState
  statusState: StepState
  percent: number
  processed?: number
  total?: number
  backendStatus?: string
  lastMessage?: string
  lastChecked?: string
  listUrl?: string
  objectUrl?: string
  statusUrl?: string
  response?: BackendPayload
}

type LogEntry = {
  id: string
  time: string
  tone: "info" | "success" | "error"
  text: string
}

const ENTITIES: Entity[] = [
  {
    key: "communication_channels",
    listKey: "communication_channels_list",
    title: "Communication Channels",
    short: "Canali",
  },
  {
    key: "integration_configurations",
    listKey: "integration_configurations_list",
    title: "Integration Configurations",
    short: "Configurazioni",
  },
  {
    key: "value_mappings",
    listKey: "value_mappings_list",
    title: "Value Mappings",
    short: "Mapping",
  },
  {
    key: "sender_agreements",
    listKey: "sender_agreements_list",
    title: "Sender Agreements",
    short: "Sender",
  },
  {
    key: "receiver_agreements",
    listKey: "receiver_agreements_list",
    title: "Receiver Agreements",
    short: "Receiver",
  },
]

const ENVIRONMENTS = ["pod", "pid", "pop", "pip"]

function initialRuntime(): Record<string, EntityRuntime> {
  return ENTITIES.reduce<Record<string, EntityRuntime>>((acc, entity) => {
    acc[entity.key] = {
      listState: "idle",
      objectState: "idle",
      statusState: "idle",
      percent: 0,
    }
    return acc
  }, {})
}

function nowLabel() {
  return new Date().toLocaleTimeString("it-IT", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  })
}

function endpoint(path: string) {
  return `/api/backend/${path.replace(/^\/+/, "")}`
}

function clampPercent(value: number) {
  if (!Number.isFinite(value)) return 0
  return Math.max(0, Math.min(100, Math.round(value)))
}

function percentFromPayload(payload?: BackendPayload) {
  if (!payload) return 0
  if (typeof payload.percent_complete === "number") return clampPercent(payload.percent_complete)
  if (typeof payload.processed === "number" && typeof payload.total === "number" && payload.total > 0) {
    return clampPercent((payload.processed / payload.total) * 100)
  }
  return payload.status === "completed" ? 100 : 0
}

function messageFromPayload(payload: BackendPayload, fallback: string) {
  if (typeof payload.message === "string") return payload.message
  if (typeof payload.detail === "string") return payload.detail
  return fallback
}

function isRunningStatus(status?: string) {
  return status === "running" || status === "started"
}

function stateLabel(state: StepState) {
  if (state === "running") return "In corso"
  if (state === "success") return "OK"
  if (state === "error") return "Errore"
  return "In attesa"
}

function backendStatusLabel(status?: string) {
  if (!status) return "Non letto"
  if (status === "not_found") return "Non trovato"
  if (status === "started") return "Avviato"
  if (status === "running") return "In corso"
  if (status === "completed") return "Completato"
  if (status === "error") return "Errore"
  return status
}

function StatusPill({ state, label }: { state: StepState; label?: string }) {
  const Icon = state === "running" ? Loader2 : state === "success" ? Check : state === "error" ? X : Clock3

  return (
    <span className={`status-pill ${state}`}>
      <Icon className={state === "running" ? "spin" : ""} size={14} />
      {label || stateLabel(state)}
    </span>
  )
}

export default function MetadataConsole() {
  const [environment, setEnvironment] = useState("pod")
  const [listMode, setListMode] = useState<"requested" | "backend">("requested")
  const [polling, setPolling] = useState(false)
  const [phase, setPhase] = useState<Phase>("idle")
  const [runtimes, setRuntimes] = useState<Record<string, EntityRuntime>>(() => initialRuntime())
  const [logs, setLogs] = useState<LogEntry[]>([])
  const pollingRef = useRef(false)
  const runtimesRef = useRef(runtimes)

  const busy = phase !== "idle" || polling
  const summary = useMemo(() => {
    const values = Object.values(runtimes)
    const average = values.length ? clampPercent(values.reduce((sum, item) => sum + item.percent, 0) / values.length) : 0
    const completed = values.filter((item) => item.backendStatus === "completed" || item.percent >= 100).length
    const errors = values.filter(
      (item) => item.listState === "error" || item.objectState === "error" || item.statusState === "error",
    ).length

    return {
      average,
      completed,
      running: values.filter((item) => isRunningStatus(item.backendStatus)).length,
      errors,
    }
  }, [runtimes])

  useEffect(() => {
    pollingRef.current = polling
  }, [polling])

  useEffect(() => {
    runtimesRef.current = runtimes
  }, [runtimes])

  function addLog(tone: LogEntry["tone"], text: string) {
    setLogs((current) => [{ id: `${Date.now()}-${Math.random()}`, time: nowLabel(), tone, text }, ...current].slice(0, 12))
  }

  function updateEntity(key: string, patch: Partial<EntityRuntime>) {
    setRuntimes((current) => ({
      ...current,
      [key]: {
        ...current[key],
        ...patch,
      },
    }))
  }

  function listPath(entity: Entity) {
    if (listMode === "backend") return `extract/${environment}/${entity.listKey}`
    return `extract/full/${environment}/${entity.listKey}`
  }

  function objectPath(entity: Entity) {
    return `extract/full/${environment}/${entity.key}/refresh`
  }

  function statusPath(entity: Entity) {
    return `extract/full/${environment}/${entity.key}/status`
  }

  async function callBackend(path: string) {
    const response = await fetch(endpoint(path), {
      method: "GET",
      cache: "no-store",
    })
    const contentType = response.headers.get("content-type") || ""
    const payload = contentType.includes("application/json")
      ? ((await response.json()) as BackendPayload)
      : ({ message: await response.text() } as BackendPayload)

    if (!response.ok) {
      throw new Error(messageFromPayload(payload, `HTTP ${response.status}`))
    }

    return payload
  }

  async function refreshLists() {
    setPhase("list")
    addLog("info", `Refresh liste avviato su ambiente ${environment}.`)

    for (const entity of ENTITIES) {
      const path = listPath(entity)
      updateEntity(entity.key, {
        listState: "running",
        listUrl: path,
        lastMessage: undefined,
      })

      try {
        const payload = await callBackend(path)
        updateEntity(entity.key, {
          listState: "success",
          response: payload,
          lastChecked: nowLabel(),
          lastMessage: messageFromPayload(payload, "Lista aggiornata."),
        })
        addLog("success", `${entity.short}: lista aggiornata.`)
      } catch (error) {
        const message = error instanceof Error ? error.message : "Errore sconosciuto"
        updateEntity(entity.key, {
          listState: "error",
          lastChecked: nowLabel(),
          lastMessage: message,
        })
        addLog("error", `${entity.short}: refresh lista fallito (${message}).`)
      }
    }

    setPhase("idle")
  }

  async function refreshObjects() {
    setPhase("object")
    addLog("info", `Refresh oggetti singoli avviato su ambiente ${environment}.`)

    await Promise.all(
      ENTITIES.map(async (entity) => {
        const path = objectPath(entity)
        updateEntity(entity.key, {
          objectState: "running",
          objectUrl: path,
          statusUrl: statusPath(entity),
          lastMessage: undefined,
        })

        try {
          const payload = await callBackend(path)
          updateEntity(entity.key, {
            objectState: "success",
            statusState: "success",
            backendStatus: payload.status,
            percent: percentFromPayload(payload),
            processed: payload.processed,
            total: payload.total,
            response: payload,
            lastChecked: nowLabel(),
            lastMessage: messageFromPayload(payload, "Refresh oggetti avviato."),
          })
          addLog("success", `${entity.short}: refresh oggetti ${backendStatusLabel(payload.status).toLowerCase()}.`)
        } catch (error) {
          const message = error instanceof Error ? error.message : "Errore sconosciuto"
          updateEntity(entity.key, {
            objectState: "error",
            statusState: "error",
            backendStatus: "error",
            lastChecked: nowLabel(),
            lastMessage: message,
          })
          addLog("error", `${entity.short}: refresh oggetti fallito (${message}).`)
        }
      }),
    )

    setPhase("idle")
    setPolling(true)
  }

  async function pollOnce(silent = false) {
    if (!silent) {
      setPhase("poll")
      addLog("info", `Controllo status su ambiente ${environment}.`)
    }

    await Promise.all(
      ENTITIES.map(async (entity) => {
        const path = statusPath(entity)
        updateEntity(entity.key, {
          statusState: "running",
          statusUrl: path,
        })

        try {
          const payload = await callBackend(path)
          updateEntity(entity.key, {
            statusState: "success",
            backendStatus: payload.status,
            percent: percentFromPayload(payload),
            processed: payload.processed,
            total: payload.total,
            response: payload,
            lastChecked: nowLabel(),
            lastMessage: messageFromPayload(payload, "Status aggiornato."),
          })
        } catch (error) {
          const message = error instanceof Error ? error.message : "Errore sconosciuto"
          updateEntity(entity.key, {
            statusState: "error",
            backendStatus: "error",
            lastChecked: nowLabel(),
            lastMessage: message,
          })
        }
      }),
    )

    if (!silent) setPhase("idle")
  }

  async function runWorkflow() {
    setPolling(false)
    setRuntimes(initialRuntime())
    setLogs([])
    await refreshLists()
    await refreshObjects()
  }

  function reset() {
    setPolling(false)
    setPhase("idle")
    setRuntimes(initialRuntime())
    setLogs([])
  }

  useEffect(() => {
    if (!polling) return

    let cancelled = false

    async function tick() {
      await pollOnce(true)

      if (cancelled || !pollingRef.current) return

      const latest = Object.values(runtimesRef.current)
      const stillRunning = latest.some((item) => isRunningStatus(item.backendStatus) || item.percent < 100)
      if (!stillRunning && latest.some((item) => item.statusState !== "idle")) {
        setPolling(false)
        addLog("success", "Polling fermato: tutti gli oggetti risultano completati o senza avanzamento pendente.")
      }
    }

    tick()
    const timer = window.setInterval(tick, 3000)

    return () => {
      cancelled = true
      window.clearInterval(timer)
    }
  }, [polling, environment])

  return (
    <main className="shell">
      <section className="topbar">
        <div>
          <p className="eyebrow">SAP PO Metadata</p>
          <h1>Console refresh e polling</h1>
        </div>
        <div className="actions">
          <label className="select-label">
            Ambiente
            <select value={environment} onChange={(event) => setEnvironment(event.target.value)} disabled={busy}>
              {ENVIRONMENTS.map((item) => (
                <option key={item} value={item}>
                  {item.toUpperCase()}
                </option>
              ))}
            </select>
          </label>
          <button className="icon-button secondary" onClick={reset} title="Reset stato locale" disabled={phase !== "idle"}>
            <RotateCcw size={18} />
          </button>
          <button className="primary-button" onClick={runWorkflow} disabled={busy}>
            {busy ? <Loader2 className="spin" size={18} /> : <Play size={18} />}
            Avvia workflow
          </button>
        </div>
      </section>

      <section className="summary-grid">
        <div className="metric main-metric">
          <div className="metric-heading">
            <DatabaseZap size={20} />
            Avanzamento medio refresh singoli
          </div>
          <strong>{summary.average}%</strong>
          <div className="progress-track large">
            <div style={{ width: `${summary.average}%` }} />
          </div>
        </div>
        <div className="metric">
          <span>Completati</span>
          <strong>{summary.completed}/5</strong>
        </div>
        <div className="metric">
          <span>In corso</span>
          <strong>{summary.running}</strong>
        </div>
        <div className="metric">
          <span>Errori</span>
          <strong>{summary.errors}</strong>
        </div>
      </section>

      <section className="control-band">
        <div className="workflow-steps">
          <div className={`workflow-step ${phase === "list" ? "active" : ""}`}>
            <Server size={18} />
            Refresh liste
          </div>
          <ChevronRight size={16} />
          <div className={`workflow-step ${phase === "object" ? "active" : ""}`}>
            <RefreshCw size={18} />
            Refresh oggetti
          </div>
          <ChevronRight size={16} />
          <div className={`workflow-step ${polling ? "active" : ""}`}>
            <Clock3 size={18} />
            Polling status
          </div>
        </div>
        <div className="inline-controls">
          <label className="select-label compact">
            Endpoint liste
            <select value={listMode} onChange={(event) => setListMode(event.target.value as "requested" | "backend")} disabled={busy}>
              <option value="requested">/extract/full/&lt;env&gt;/..._list</option>
              <option value="backend">/extract/&lt;env&gt;/..._list</option>
            </select>
          </label>
          <button onClick={refreshLists} disabled={busy}>
            <Server size={17} />
            Solo liste
          </button>
          <button onClick={refreshObjects} disabled={busy}>
            <RefreshCw size={17} />
            Solo oggetti
          </button>
          <button onClick={() => pollOnce()} disabled={phase !== "idle"}>
            <Settings2 size={17} />
            Status ora
          </button>
          <button onClick={() => setPolling((current) => !current)} disabled={phase !== "idle"}>
            {polling ? <Pause size={17} /> : <Play size={17} />}
            {polling ? "Pausa polling" : "Avvia polling"}
          </button>
        </div>
      </section>

      <section className="entity-grid">
        {ENTITIES.map((entity) => {
          const runtime = runtimes[entity.key]
          return (
            <article className="entity-card" key={entity.key}>
              <div className="entity-header">
                <div>
                  <p>{entity.short}</p>
                  <h2>{entity.title}</h2>
                </div>
                <span className={`backend-status ${runtime.backendStatus || "idle"}`}>
                  {backendStatusLabel(runtime.backendStatus)}
                </span>
              </div>

              <div className="entity-progress">
                <div className="progress-line">
                  <span>{runtime.percent}%</span>
                  <span>
                    {runtime.processed ?? 0}/{runtime.total ?? 0}
                  </span>
                </div>
                <div className="progress-track">
                  <div style={{ width: `${runtime.percent}%` }} />
                </div>
              </div>

              <div className="state-row">
                <StatusPill state={runtime.listState} label="Lista" />
                <StatusPill state={runtime.objectState} label="Oggetti" />
                <StatusPill state={runtime.statusState} label="Status" />
              </div>

              <dl className="endpoint-list">
                <div>
                  <dt>Lista</dt>
                  <dd>{runtime.listUrl || listPath(entity)}</dd>
                </div>
                <div>
                  <dt>Refresh</dt>
                  <dd>{runtime.objectUrl || objectPath(entity)}</dd>
                </div>
                <div>
                  <dt>Status</dt>
                  <dd>{runtime.statusUrl || statusPath(entity)}</dd>
                </div>
              </dl>

              <div className="card-footer">
                <span>{runtime.lastChecked ? `Ultimo check ${runtime.lastChecked}` : "Nessun check eseguito"}</span>
                {runtime.lastMessage && (
                  <span className={runtime.backendStatus === "error" ? "message error" : "message"}>{runtime.lastMessage}</span>
                )}
              </div>
            </article>
          )
        })}
      </section>

      <section className="log-panel">
        <div className="panel-title">
          <AlertTriangle size={18} />
          Eventi
        </div>
        {logs.length === 0 ? (
          <p className="empty">Gli eventi del workflow compariranno qui.</p>
        ) : (
          <ul>
            {logs.map((entry) => (
              <li className={entry.tone} key={entry.id}>
                <time>{entry.time}</time>
                <span>{entry.text}</span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  )
}
