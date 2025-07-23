import { useEffect, useState, useRef } from "react";

export default function useAsync(fn, deps = [], enabled = true) {
  const [data, setData]     = useState(null);
  const [error, setError]   = useState(null);
  const [loading, setLoad]  = useState(false);
  const abortRef = useRef();

  useEffect(() => {
    if (!enabled) return;

    const controller = new AbortController();
    abortRef.current = controller;

    let mounted = true;
    setLoad(true); setError(null);

    fn({ signal: controller.signal })
      .then(res => { if (mounted) setData(res); })
      .catch(err => { if (mounted && err.name !== "CanceledError") setError(err); })
      .finally(() => mounted && setLoad(false));

    return () => { mounted = false; controller.abort(); };
  }, deps);

  return { data, error, loading };
}
