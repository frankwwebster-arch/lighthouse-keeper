/** @type {import('next').NextConfig} */
export default {
  reactStrictMode: true,
  async redirects() {
    return [
      {
        source: '/keeper-review',
        destination: '/keeper-review/index.html',
        permanent: false,
      },
    ]
  },
}
