const DEFAULT_BACKEND_BASE_URL = "http://127.0.0.1:5001"

type RouteContext = {
  params: Promise<{
    path: string[]
  }>
}

async function proxy(request: Request, context: RouteContext) {
  const { path } = await context.params
  const baseUrl = (process.env.BACKEND_BASE_URL || DEFAULT_BACKEND_BASE_URL).replace(/\/$/, "")
  const upstreamPath = path.map(encodeURIComponent).join("/")
  const upstreamUrl = `${baseUrl}/${upstreamPath}${new URL(request.url).search}`

  try {
    const response = await fetch(upstreamUrl, {
      method: request.method,
      cache: "no-store",
      headers: {
        accept: "application/json",
      },
    })

    const contentType = response.headers.get("content-type") || "application/json"
    const body = await response.text()

    return new Response(body, {
      status: response.status,
      headers: {
        "content-type": contentType,
      },
    })
  } catch (error) {
    const message = error instanceof Error ? error.message : "Errore sconosciuto"

    return Response.json(
      {
        status: "error",
        message: `Backend non raggiungibile: ${message}`,
      },
      { status: 502 },
    )
  }
}

export async function GET(request: Request, context: RouteContext) {
  return proxy(request, context)
}

export async function POST(request: Request, context: RouteContext) {
  return proxy(request, context)
}
