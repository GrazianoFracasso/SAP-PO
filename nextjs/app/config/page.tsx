import { AdminLayout } from "@/components/admin-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Switch } from "@/components/ui/switch"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Save, RefreshCw, AlertTriangle } from "lucide-react"

export default function ConfigPage() {
  return (
    <AdminLayout>
      <div className="p-6 space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">Configurazione</h1>
            <p className="text-muted-foreground">Gestisci le impostazioni del sistema SAP PO Metadata Tool</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline">
              <RefreshCw className="h-4 w-4 mr-2" />
              Reset
            </Button>
            <Button>
              <Save className="h-4 w-4 mr-2" />
              Salva Modifiche
            </Button>
          </div>
        </div>

        <Tabs defaultValue="general" className="space-y-4">
          <TabsList>
            <TabsTrigger value="general">Generale</TabsTrigger>
            <TabsTrigger value="sap">SAP PO</TabsTrigger>
            <TabsTrigger value="database">Database</TabsTrigger>
            <TabsTrigger value="security">Sicurezza</TabsTrigger>
            <TabsTrigger value="notifications">Notifiche</TabsTrigger>
          </TabsList>

          <TabsContent value="general" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Impostazioni Generali</CardTitle>
                <CardDescription>Configurazione base del sistema</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="app-name">Nome Applicazione</Label>
                    <Input id="app-name" defaultValue="SAP PO Metadata Tool" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="environment">Ambiente</Label>
                    <Select defaultValue="production">
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="development">Development</SelectItem>
                        <SelectItem value="staging">Staging</SelectItem>
                        <SelectItem value="production">Production</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="description">Descrizione</Label>
                  <Textarea
                    id="description"
                    defaultValue="Tool per l'estrazione e gestione dei metadati da SAP Process Orchestration"
                    rows={3}
                  />
                </div>

                <div className="flex items-center space-x-2">
                  <Switch id="debug-mode" />
                  <Label htmlFor="debug-mode">Modalità Debug</Label>
                </div>

                <div className="flex items-center space-x-2">
                  <Switch id="maintenance-mode" />
                  <Label htmlFor="maintenance-mode">Modalità Manutenzione</Label>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Impostazioni Performance</CardTitle>
                <CardDescription>Configurazione delle performance del sistema</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="max-connections">Max Connessioni Simultanee</Label>
                    <Input id="max-connections" type="number" defaultValue="50" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="timeout">Timeout (secondi)</Label>
                    <Input id="timeout" type="number" defaultValue="30" />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="batch-size">Dimensione Batch</Label>
                    <Input id="batch-size" type="number" defaultValue="100" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="retry-attempts">Tentativi di Retry</Label>
                    <Input id="retry-attempts" type="number" defaultValue="3" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="sap" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Configurazione SAP PO</CardTitle>
                <CardDescription>Impostazioni per la connessione a SAP Process Orchestration</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="sap-host">Host SAP PO</Label>
                    <Input id="sap-host" defaultValue="po-prod.company.com" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="sap-port">Porta</Label>
                    <Input id="sap-port" type="number" defaultValue="8000" />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="sap-client">Client</Label>
                    <Input id="sap-client" defaultValue="100" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="sap-language">Lingua</Label>
                    <Select defaultValue="IT">
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="IT">Italiano</SelectItem>
                        <SelectItem value="EN">English</SelectItem>
                        <SelectItem value="DE">Deutsch</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="sap-username">Username</Label>
                  <Input id="sap-username" defaultValue="METADATA_USER" />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="sap-password">Password</Label>
                  <Input id="sap-password" type="password" placeholder="••••••••" />
                </div>

                <div className="flex items-center space-x-2">
                  <Switch id="sap-ssl" defaultChecked />
                  <Label htmlFor="sap-ssl">Usa SSL/TLS</Label>
                </div>

                <Button variant="outline" className="w-full">
                  Testa Connessione
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Configurazione Metadata Extraction</CardTitle>
                <CardDescription>Impostazioni per l'estrazione dei metadati</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="extraction-schedule">Pianificazione Estrazione</Label>
                  <Select defaultValue="daily">
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="hourly">Ogni ora</SelectItem>
                      <SelectItem value="daily">Giornaliera</SelectItem>
                      <SelectItem value="weekly">Settimanale</SelectItem>
                      <SelectItem value="manual">Manuale</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="extraction-time">Orario Estrazione</Label>
                  <Input id="extraction-time" type="time" defaultValue="02:00" />
                </div>

                <div className="flex items-center space-x-2">
                  <Switch id="incremental-extraction" defaultChecked />
                  <Label htmlFor="incremental-extraction">Estrazione Incrementale</Label>
                </div>

                <div className="flex items-center space-x-2">
                  <Switch id="validate-metadata" defaultChecked />
                  <Label htmlFor="validate-metadata">Validazione Metadati</Label>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="database" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Configurazione Database</CardTitle>
                <CardDescription>Impostazioni per la connessione al database</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="db-host">Host Database</Label>
                    <Input id="db-host" defaultValue="localhost" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="db-port">Porta</Label>
                    <Input id="db-port" type="number" defaultValue="5432" />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="db-name">Nome Database</Label>
                    <Input id="db-name" defaultValue="sap_metadata" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="db-schema">Schema</Label>
                    <Input id="db-schema" defaultValue="public" />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="db-username">Username</Label>
                    <Input id="db-username" defaultValue="metadata_user" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="db-password">Password</Label>
                    <Input id="db-password" type="password" placeholder="••••••••" />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="db-pool-min">Pool Min Connections</Label>
                    <Input id="db-pool-min" type="number" defaultValue="5" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="db-pool-max">Pool Max Connections</Label>
                    <Input id="db-pool-max" type="number" defaultValue="20" />
                  </div>
                </div>

                <Button variant="outline" className="w-full">
                  Testa Connessione Database
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="security" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Impostazioni Sicurezza</CardTitle>
                <CardDescription>Configurazione della sicurezza e autenticazione</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center space-x-2">
                  <Switch id="enable-auth" defaultChecked />
                  <Label htmlFor="enable-auth">Abilita Autenticazione</Label>
                </div>

                <div className="flex items-center space-x-2">
                  <Switch id="enable-2fa" />
                  <Label htmlFor="enable-2fa">Autenticazione a Due Fattori</Label>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="session-timeout">Timeout Sessione (minuti)</Label>
                  <Input id="session-timeout" type="number" defaultValue="60" />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="password-policy">Policy Password</Label>
                  <Select defaultValue="medium">
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="low">Bassa</SelectItem>
                      <SelectItem value="medium">Media</SelectItem>
                      <SelectItem value="high">Alta</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex items-center space-x-2">
                  <Switch id="audit-logging" defaultChecked />
                  <Label htmlFor="audit-logging">Audit Logging</Label>
                </div>

                <div className="flex items-center space-x-2">
                  <Switch id="ip-whitelist" />
                  <Label htmlFor="ip-whitelist">Whitelist IP</Label>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="notifications" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Configurazione Notifiche</CardTitle>
                <CardDescription>Impostazioni per le notifiche del sistema</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center space-x-2">
                  <Switch id="email-notifications" defaultChecked />
                  <Label htmlFor="email-notifications">Notifiche Email</Label>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="smtp-server">Server SMTP</Label>
                  <Input id="smtp-server" defaultValue="smtp.company.com" />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="smtp-port">Porta SMTP</Label>
                    <Input id="smtp-port" type="number" defaultValue="587" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="smtp-security">Sicurezza</Label>
                    <Select defaultValue="tls">
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="none">Nessuna</SelectItem>
                        <SelectItem value="tls">TLS</SelectItem>
                        <SelectItem value="ssl">SSL</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="notification-email">Email Notifiche</Label>
                  <Input id="notification-email" type="email" defaultValue="admin@company.com" />
                </div>

                <div className="space-y-4">
                  <Label>Tipi di Notifica</Label>
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2">
                      <Switch id="notify-errors" defaultChecked />
                      <Label htmlFor="notify-errors">Errori di Sistema</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Switch id="notify-warnings" defaultChecked />
                      <Label htmlFor="notify-warnings">Avvisi</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Switch id="notify-success" />
                      <Label htmlFor="notify-success">Operazioni Completate</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Switch id="notify-maintenance" defaultChecked />
                      <Label htmlFor="notify-maintenance">Manutenzione Programmata</Label>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        <div className="flex items-center gap-2 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <AlertTriangle className="h-5 w-5 text-yellow-600" />
          <p className="text-sm text-yellow-800">
            Le modifiche alla configurazione richiederanno il riavvio del servizio per essere applicate.
          </p>
        </div>
      </div>
    </AdminLayout>
  )
}
