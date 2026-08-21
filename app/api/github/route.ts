import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const username = request.nextUrl.searchParams.get("username")?.trim();
  if (!username) return NextResponse.json({ ok: false }, { status: 400 });
  try {
    const headers = { Accept: "application/vnd.github+json" };
    const [profileResponse, reposResponse] = await Promise.all([
      fetch(`https://api.github.com/users/${encodeURIComponent(username)}`, { headers, next: { revalidate: 3600 } }),
      fetch(`https://api.github.com/users/${encodeURIComponent(username)}/repos?per_page=100&sort=updated`, { headers, next: { revalidate: 3600 } })
    ]);
    if (!profileResponse.ok || !reposResponse.ok) return NextResponse.json({ ok: false }, { status: 404 });
    const profile = await profileResponse.json();
    const repos = await reposResponse.json();
    const topLanguages = [...new Set(repos.map((repo: { language: string | null }) => repo.language).filter(Boolean))].slice(0, 5);
    return NextResponse.json({ ok: true, name: profile.name || profile.login, publicRepos: profile.public_repos, topLanguages });
  } catch { return NextResponse.json({ ok: false }, { status: 502 }); }
}
