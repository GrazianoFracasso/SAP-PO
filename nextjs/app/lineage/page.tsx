import { AdminLayout } from "@/components/admin-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { GitBranch, Search, Filter, Download, ArrowRight, Database, FileText, Workflow } from "lucide-react"

export default function LineagePage() {
  return (
    <AdminLayout>
      <div className="p-6 space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">Data Lineage</h1>
            <p className="text-muted-foreground">Tracciabilità e genealogia dei metadati SAP PO</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline">
              <Filter className="h-4 w-4 mr-2" />
              Filtri
            </Button>
            <Button variant="outline">
              <Download className="h-4 w-4 mr-2" />
              Esporta
            </Button>
          </div>
        </div>

        {/* Search and Filters */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Search className="h-5 w-5" />
              Ricerca Lineage
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex gap-4">
              <div className="flex-1">
                <Input placeholder="Cerca per nome oggetto, interfaccia, o mapping..." />
              </div>
              <Select defaultValue="all">
                <SelectTrigger className="w-48">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Tutti i Tipi</SelectItem>
                  <SelectItem value="interface">Interface</SelectItem>
                  <SelectItem value="mapping">Message Mapping</SelectItem>
                  <SelectItem value="channel">Communication Channel</SelectItem>
                  <SelectItem value="agreement">Agreement</SelectItem>
                </SelectContent>
              </Select>
              <Button>
                <Search className="h-4 w-4 mr-2" />
                Cerca
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Lineage Overview */}
        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <Database className="h-4 w-4" />
                Oggetti Tracciati
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">1,247</div>
              <p className="text-xs text-muted-foreground">+23 questa settimana</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <GitBranch className="h-4 w-4" />
                Relazioni Mappate
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">3,891</div>
              <p className="text-xs text-muted-foreground">+67 questa settimana</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <Workflow className="h-4 w-4" />
                Flussi Completi
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">156</div>
              <p className="text-xs text-muted-foreground">+8 questa settimana</p>
            </CardContent>
          </Card>
        </div>

        {/* Lineage Tree Example */}
        <Card>
          <CardHeader>
            <CardTitle>Esempio Lineage: Order Processing Flow</CardTitle>
            <CardDescription>Tracciabilità completa del flusso di elaborazione ordini</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {/* Source Systems */}
              <div className="flex items-center gap-4">
                <div className="w-32 text-sm font-medium text-muted-foreground">Source</div>
                <div className="flex items-center gap-2">
                  <div className="p-3 border rounded-lg bg-blue-50">
                    <Database className="h-4 w-4 text-blue-600" />
                  </div>
                  <div>
                    <p className="font-medium">SAP ECC</p>
                    <p className="text-xs text-muted-foreground">Order Management</p>
                  </div>
                </div>
                <ArrowRight className="h-4 w-4 text-muted-foreground" />
                <div className="flex items-center gap-2">
                  <div className="p-3 border rounded-lg bg-green-50">
                    <FileText className="h-4 w-4 text-green-600" />
                  </div>
                  <div>
                    <p className="font-medium">ORDERS05</p>
                    <p className="text-xs text-muted-foreground">IDoc Interface</p>
                  </div>
                </div>
              </div>

              {/* Processing Layer */}
              <div className="flex items-center gap-4">
                <div className="w-32 text-sm font-medium text-muted-foreground">Processing</div>
                <div className="flex items-center gap-2">
                  <div className="p-3 border rounded-lg bg-purple-50">
                    <Workflow className="h-4 w-4 text-purple-600" />
                  </div>
                  <div>
                    <p className="font-medium">OrderTransformation</p>
                    <p className="text-xs text-muted-foreground">Message Mapping</p>
                  </div>
                </div>
                <ArrowRight className="h-4 w-4 text-muted-foreground" />
                <div className="flex items-center gap-2">
                  <div className="p-3 border rounded-lg bg-orange-50">
                    <GitBranch className="h-4 w-4 text-orange-600" />
                  </div>
                  <div>
                    <p className="font-medium">OrderValidation</p>
                    <p className="text-xs text-muted-foreground">Java Mapping</p>
                  </div>
                </div>
              </div>

              {/* Target Systems */}
              <div className="flex items-center gap-4">
                <div className="w-32 text-sm font-medium text-muted-foreground">Target</div>
                <div className="flex items-center gap-2">
                  <div className="p-3 border rounded-lg bg-red-50">
                    <Database className="h-4 w-4 text-red-600" />
                  </div>
                  <div>
                    <p className="font-medium">CRM System</p>
                    <p className="text-xs text-muted-foreground">Customer Orders</p>
                  </div>
                </div>
                <ArrowRight className="h-4 w-4 text-muted-foreground" />
                <div className="flex items-center gap-2">
                  <div className="p-3 border rounded-lg bg-teal-50">
                    <Database className="h-4 w-4 text-teal-600" />
                  </div>
                  <div>
                    <p className="font-medium">Warehouse System</p>
                    <p className="text-xs text-muted-foreground">Inventory Update</p>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Recent Lineage Changes */}
        <Card>
          <CardHeader>
            <CardTitle>Modifiche Recenti al Lineage</CardTitle>
            <CardDescription>Ultime modifiche alla tracciabilità dei dati</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <div>
                    <p className="font-medium">Nuovo mapping aggiunto</p>
                    <p className="text-sm text-muted-foreground">CustomerData_Transform → CRM_Interface</p>
                  </div>
                </div>
                <div className="text-right">
                  <Badge variant="secondary" className="bg-green-100 text-green-800">
                    Aggiunto
                  </Badge>
                  <p className="text-xs text-muted-foreground mt-1">2 ore fa</p>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <div>
                    <p className="font-medium">Relazione aggiornata</p>
                    <p className="text-sm text-muted-foreground">OrderProcessing → InventoryUpdate</p>
                  </div>
                </div>
                <div className="text-right">
                  <Badge variant="secondary" className="bg-blue-100 text-blue-800">
                    Modificato
                  </Badge>
                  <p className="text-xs text-muted-foreground mt-1">5 ore fa</p>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                  <div>
                    <p className="font-medium">Oggetto rimosso</p>
                    <p className="text-sm text-muted-foreground">LegacyOrderInterface (deprecato)</p>
                  </div>
                </div>
                <div className="text-right">
                  <Badge variant="destructive">Rimosso</Badge>
                  <p className="text-xs text-muted-foreground mt-1">1 giorno fa</p>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                  <div>
                    <p className="font-medium">Nuovo flusso completo</p>
                    <p className="text-sm text-muted-foreground">Invoice Processing End-to-End</p>
                  </div>
                </div>
                <div className="text-right">
                  <Badge variant="secondary" className="bg-purple-100 text-purple-800">
                    Flusso
                  </Badge>
                  <p className="text-xs text-muted-foreground mt-1">2 giorni fa</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Lineage Statistics */}
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Statistiche per Tipo</CardTitle>
              <CardDescription>Distribuzione degli oggetti tracciati</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm">Message Interfaces</span>
                <div className="flex items-center gap-2">
                  <div className="w-24 bg-muted rounded-full h-2">
                    <div className="bg-blue-500 h-2 rounded-full" style={{ width: "45%" }}></div>
                  </div>
                  <span className="text-sm font-medium">456</span>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm">Message Mappings</span>
                <div className="flex items-center gap-2">
                  <div className="w-24 bg-muted rounded-full h-2">
                    <div className="bg-green-500 h-2 rounded-full" style={{ width: "35%" }}></div>
                  </div>
                  <span className="text-sm font-medium">342</span>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm">Communication Channels</span>
                <div className="flex items-center gap-2">
                  <div className="w-24 bg-muted rounded-full h-2">
                    <div className="bg-purple-500 h-2 rounded-full" style={{ width: "25%" }}></div>
                  </div>
                  <span className="text-sm font-medium">234</span>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm">Agreements</span>
                <div className="flex items-center gap-2">
                  <div className="w-24 bg-muted rounded-full h-2">
                    <div className="bg-orange-500 h-2 rounded-full" style={{ width: "20%" }}></div>
                  </div>
                  <span className="text-sm font-medium">215</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Complessità Flussi</CardTitle>
              <CardDescription>Analisi della complessità dei flussi di dati</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm">Flussi Semplici (1-3 step)</span>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary" className="bg-green-100 text-green-800">
                    89
                  </Badge>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm">Flussi Medi (4-7 step)</span>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary" className="bg-yellow-100 text-yellow-800">
                    45
                  </Badge>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm">Flussi Complessi (8+ step)</span>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary" className="bg-red-100 text-red-800">
                    22
                  </Badge>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm">Flussi Orfani</span>
                <div className="flex items-center gap-2">
                  <Badge variant="destructive">3</Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </AdminLayout>
  )
}
