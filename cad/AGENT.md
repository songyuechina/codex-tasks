# CAD項目規範

**版本**: v1.4
**更新日期**: 2025-11-18
**適用範圍**: D:/codex-tasks/cad

---

## 第一規範：CAD 即時對話要求

### 快捷命令

- jst：等效於執行指令“按即时对话.txt的内容执行”，即按照 cad/即时对话.txt 的所有流程要求來操作。遇到該命令時，必須立即依照即时对话規範完成導入、七個基礎范式與後續流程。


來源：`D:/codex-tasks/cad/即时对话.txt`。凡在 CAD 項目內進行文件操作、函數開發或測試，必須遵守：

1. **基礎導入**（任務開始即執行）：
   ```python
   from CAD_basic import *
   from CAD_file_operations import *
   ```
2. **七個基礎范式**（每步都需 `cad_zt_zero()` 清場，並保存/關閉）：  
   - 新建 DWG → 畫線 → 保存 → 關閉  
   - 打開 DWG → 畫圓 → 保存 → 關閉
   - `copy_file_content_pywin32(B, A)` 整體插入
   - `insert_region_from_file(...)` 區域對齊插入
   - `draw_tarch_wall(...)`
   - `insert_tarch_door(...)`
   - `insert_tarch_window(...)`
3. **必用接口**：區域選擇 `select_entities_in_window`；圖層選擇 `stc`；屬性讀寫 `get_object_property`/`set_object_property`。
4. **日誌與迭代**：每個步驟須打印提示，錯誤後必須根據反饋修正並重測直至成功。
5. **函數資料夾**：每個函數都要在 Functional_control 對應目錄內建立獨立資料夾，包含函數實現、測試腳本、測試 DWG 副本與測試記錄（tests/logs/scripts 等），並記錄每輪測試的日期、DWG 副本名稱、坐標/厚度配置與結果（存放於 tests/logs）。若同一資料夾涵蓋多個函數（如 insert_tests），必須建立對應子資料夾避免互相覆寫，且每個子資料夾都需備有 README.md（第一行為完整命令列示例）、測試腳本需以命令列傳入參數，並在每次測試後透過 shared 模板還原 DWG 初始狀態，確保命令可重複執行。同時所有測試腳本必須遵循 `cad_zt_oneb()` → `litz()` → 執行函數 → 關閉相關文件 → `cad_zt_oneb()` 的流程，確保開始與結束都回到「天正啟動且打開未保存 DWG」的基準狀態。
6. **超時回退（命令級）**：任何單條 CAD 命令阻塞超過 120 秒，立即執行 cad_zt_zero() 回 0 進程後重試；適用於命令，不是整體函數流程。
5. **超時回退（命令級）**：任何單條 CAD 命令阻塞超過 120 秒，立即執行 `cad_zt_zero()` 回到 0 進程初始狀態後再重試；此限制作用於每次命令發送，而非整個函數流程。

---

## 其他規範

（保留原強制/條件規則與測試、佈局要求。若有衝突，第一規範優先級僅次於強制執行規則。）




