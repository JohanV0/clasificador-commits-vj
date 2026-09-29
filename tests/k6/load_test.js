import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 5 },   // sube a 5 usuarios
    { duration: '20s', target: 10 },  // sube a 10 usuarios
    { duration: '10s', target: 0 },   // baja a 0
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'],  // 95% de requests < 2s
    http_req_failed: ['rate<0.05'],     // menos del 5% de errores
  },
};

export default function () {
  const res = http.get('http://localhost:8000/commits');
  check(res, {
    'status 200': (r) => r.status === 200,
    'tiempo < 2s': (r) => r.timings.duration < 2000,
  });
  sleep(1);
}
