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
      {
        source: '/keeper-review/keeper-prime-master-v1',
        destination: '/keeper-review/keeper-prime-master-v1/index.html',
        permanent: false,
      },
      {
        source: '/keeper-review/keeper-prime-orthographic-v1',
        destination: '/keeper-review/keeper-prime-orthographic-v1/index.html',
        permanent: false,
      },
      {
        source: '/keeper-review/keeper-prime-orthographic-v2',
        destination: '/keeper-review/keeper-prime-orthographic-v2/index.html',
        permanent: false,
      },
    ]
  },
}
