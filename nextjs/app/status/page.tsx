import { AdminLayout } from "@/components/admin-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { CheckCircle, AlertTriangle, XCircle, RefreshCw, Server, Database, Wifi } from "lucide-react"

export default function StatusPage() {
  return (
    <AdminLayout>
      <div className="p-6 space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">Status Sistema</h1>
            <p className="text-muted-foreground">Monitoraggio in tempo reale dei servizi e connessioni</p>
          </div>
          <Button>
            <RefreshCw className="h-4 w-4 mr-2" />
            Aggiorna
          </Button>
        </div>

        {/* Overall Status */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle className="h-5 w-5 text-green-500" />
              Stato Generale: Operativo
            </CardTitle>
            <CardDescription>Tutti i servizi principali sono funzionanti</CardDescription>
          </CardHeader>
        </Card>

        {/* Services Status */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <Server className="h-4 w-4" />
                SAP PO Service
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between mb-2">
                <Badge variant="secondary" className="bg-green-100 text-green-800">
                  <CheckCircle className="h-3 w-3 mr-1" />
                  Online
                </Badge>
                <span className="text-sm text-muted-foreground">99.9% uptime</span>
              </div>
              <p className="text-xs text-muted-foreground">Ultimo check: 30 secondi fa</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <Database className="h-4 w-4" />
                Database
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between mb-2">
                <Badge variant="secondary" className="bg-green-100 text-green-800">
                  <CheckCircle className="h-3 w-3 mr-1" />
                  Healthy
                </Badge>
                <span className="text-sm text-muted-foreground">Response: 12ms</span>
              </div>
              <p className="text-xs text-muted-foreground">Ultimo check: 15 secondi fa</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <Wifi className="h-4 w-4" />
                API Gateway
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between mb-2">
                <Badge variant="secondary" className="bg-yellow-100 text-yellow-800">
                  <AlertTriangle className="h-3 w-3 mr-1" />
                  Slow
                </Badge>
                <span className="text-sm text-muted-foreground">Response: 450ms</span>
              </div>
              <p className="text-xs text-muted-foreground">Ultimo check: 1 minuto fa</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <RefreshCw className="h-4 w-4" />
                Metadata Sync
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between mb-2">
                <Badge variant="secondary" className="bg-green-100 text-green-800">
                  <CheckCircle className="h-3 w-3 mr-1" />
                  Running
                </Badge>
                <span className="text-sm text-muted-foreground">Last sync: 5 min</span>
              </div>
              <p className="text-xs text-muted-foreground">Prossimo sync: 10 minuti</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <Server className="h-4 w-4" />
                Backup Service
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between mb-2">
                <Badge variant="destructive">
                  <XCircle className="h-3 w-3 mr-1" />
                  Error
                </Badge>
                <span className="text-sm text-muted-foreground">Failed at 02:30</span>
              </div>
              <p className="text-xs text-muted-foreground">Errore: Spazio insufficiente</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <Database className="h-4 w-4" />
                Cache Service
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between mb-2">
                <Badge variant="secondary" className="bg-green-100 text-green-800">
                  <CheckCircle className="h-3 w-3 mr-1" />
                  Active
                </Badge>
                <span className="text-sm text-muted-foreground">Hit rate: 94%</span>
              </div>
              <p className="text-xs text-muted-foreground">Cache size: 2.3 GB</p>
            </CardContent>
          </Card>
        </div>

        {/* Connection Status */}
        <Card>
          <CardHeader>
            <CardTitle>Stato Connessioni SAP</CardTitle>
            <CardDescription>Monitoraggio delle connessioni ai sistemi SAP</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center gap-3">
                  <CheckCircle className="h-5 w-5 text-green-500" />
                  <div>
                    <p className="font-medium">SAP PO Development</p>
                    <p className="text-sm text-muted-foreground">po-dev.company.com:8000</p>
                  </div>
                </div>
                <div className="text-right">
                  <Badge variant="secondary" className="bg-green-100 text-green-800">
                    Connected
                  </Badge>
                  <p className="text-xs text-muted-foreground mt-1">Latency: 23ms</p>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center gap-3">
                  <CheckCircle className="h-5 w-5 text-green-500" />
                  <div>
                    <p className="font-medium">SAP PO Production</p>
                    <p className="text-sm text-muted-foreground">po-prod.company.com:8000</p>
                  </div>
                </div>
                <div className="text-right">
                  <Badge variant="secondary" className="bg-green-100 text-green-800">
                    Connected
                  </Badge>
                  <p className="text-xs text-muted-foreground mt-1">Latency: 18ms</p>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center gap-3">
                  <AlertTriangle className="h-5 w-5 text-yellow-500" />
                  <div>
                    <p className="font-medium">SAP PO Test</p>
                    <p className="text-sm text-muted-foreground">po-test.company.com:8000</p>
                  </div>
                </div>
                <div className="text-right">
                  <Badge variant="secondary" className="bg-yellow-100 text-yellow-800">
                    Timeout
                  </Badge>
                  <p className="text-xs text-muted-foreground mt-1">Latency: 2.3s</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Recent Incidents */}
        <Card>
          <CardHeader>
            <CardTitle>Incidenti Recenti</CardTitle>
            <CardDescription>Cronologia degli ultimi problemi risolti</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-start gap-3 p-3 border rounded-lg">
                <XCircle className="h-5 w-5 text-red-500 mt-0.5" />
                <div className="flex-1">
                  <p className="font-medium">Backup Service Failure</p>
                  <p className="text-sm text-muted-foreground">
                    Il servizio di backup è fallito per spazio insufficiente
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">2 ore fa • Durata: 15 minuti</p>
                </div>
                <Badge variant="destructive">Risolto</Badge>
              </div>

              <div className="flex items-start gap-3 p-3 border rounded-lg">
                <AlertTriangle className="h-5 w-5 text-yellow-500 mt-0.5" />
                <div className="flex-1">
                  <p className="font-medium">High API Response Time</p>
                  <p className="text-sm text-muted-foreground">Tempi di risposta API superiori alla soglia normale</p>
                  <p className="text-xs text-muted-foreground mt-1">1 giorno fa • Durata: 45 minuti</p>
                </div>
                <Badge variant="secondary" className="bg-green-100 text-green-800">
                  Risolto
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </AdminLayout>
  )
}
