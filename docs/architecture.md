# Architecture

```
bootstrap/entry.py
      │
      ├─ core/process_attach.py  → OpenProcess on eldenring.exe
      ├─ core/memory_engine.py   → RPM/WPM primitives
      ├─ core/signature_scanner.py → AOB scans for struct bases
      │
      ├─ handlers/*              → feature-specific patchers
      │      stats_handler
      │      inventory_handler
      │      teleport_handler
      │
      ├─ overlay/shell.py        → tkinter dev UI
      └─ shared/ipc_bus.py ──────┐
                                 ▼
                        erdtree_native/OverlayHost.csproj
                        (WPF overlay, hotkey forwarding)
```

Handlers are stateless with respect to each other — they only share the
`MemoryEngine` and a resolved `player_base`. Anything that requires frame
sync (teleport) queues through the bus so the engine doesn't tear writes
mid-tick.