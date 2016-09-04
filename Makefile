POWERLINE=https://github.com/Lokaltog/vim-powerline 
PATCHER=tmp/vim-powerline/fontpatcher/fontpatcher

all:
	@echo "\033[31m"
	@echo "@@@@@@@@@@@@@@@@@ WARNING @@@@@@@@@@@@@@@@@@@"
	@echo "@ OUTPUT FONT SHOULD BE KEPT IN PRIVATE USE @"
	@echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
	@echo "\033[0m"
	make regular
	make bold

regular: merge.py tmp/scod-regular.ttf src/migu-1m-regular.ttf tmp/symbols.sfd
	fontforge -script $+ Regular full
	fontforge -script $+ Regular half

bold: merge.py tmp/scod-bold.ttf src/migu-1m-bold.ttf tmp/symbols.sfd
	fontforge -script $+ Bold full
	fontforge -script $+ Bold half

tmp/symbols.sfd: symbol.py src/SourceCodePro-Regular.ttf 
	fontforge -script $+ $@

tmp/scod-regular.ttf: src/SourceCodePro-Regular.ttf
	make patch NAME=SourceCodePro-Regular DEST=$@

tmp/scod-bold.ttf: src/SourceCodePro-Bold.ttf
	make patch NAME=SourceCodePro-Bold DEST=$@

patch: $(PATCHER)
	ROOT=$$(pwd) && cd tmp && \
	fontforge -script $$ROOT/$< $$ROOT/src/$$NAME.ttf && \
	mv $$ROOT/tmp/$$NAME-Powerline.ttf $$ROOT/$$DEST

$(PATCHER):
	@if [ ! -d tmp ]; then mkdir tmp; fi
	@if [ ! -d tmp/vim-powerline ]; then \
		git clone $(POWERLINE) tmp/vim-powerline; \
	fi

clean:
	@rm -rf tmp/*.ttf tmp/*.sfd*
	@rm -f dest/*.ttf

cleanall:
	@rm -rf tmp
	@rm -rf dest

airline:
	@if [ ! -d tmp/vim-airline ]; then \
		git clone https://github.com/vim-airline/vim-airline tmp/vim-airline; \
	fi
	@echo "\nThe following special characters are used in vim-airline:"
	@grep -rhoE \\\\u[0-9a-zA-Z]+ tmp/vim-airline/* | sort | uniq
