import runpy
import sys


def patch_colorama_flush():
    """Ensure colorama flush failures don't abort test scripts."""
    try:
        import colorama.ansitowin32 as aw  # type: ignore
    except ImportError:
        return

    original_write_plain = aw.AnsiToWin32.write_plain_text

    def safe_write_plain_text(self, text, start, end):
        if start < end:
            self.wrapped.write(text[start:end])
            try:
                self.wrapped.flush()
            except OSError:
                return None

    aw.AnsiToWin32.write_plain_text = safe_write_plain_text

    def safe_write(self, text):
        if self.strip or self.convert:
            self.write_and_convert(text)
        else:
            self.wrapped.write(text)
            try:
                self.wrapped.flush()
            except OSError:
                return None
        if self.autoreset:
            self.reset_all()

    aw.AnsiToWin32.write = safe_write


def main():
    if len(sys.argv) < 2:
        raise SystemExit("用法: python run_with_patch.py <script_path>")

    patch_colorama_flush()
    target = sys.argv[1]
    runpy.run_path(target, run_name="__main__")


if __name__ == "__main__":
    main()
