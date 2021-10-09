CC := g++
C_FLAGS := -O2 -Wall -std=c++14 -pedantic -Wshadow -Wformat=2 -Wfloat-equal -Wconversion
C_SRCS := $(wildcard src/*.cpp)
INCLUDE_PATH := ./
HEADERS := $(wildcard include/*.h)

move_gen: cpplint $(C_SRCS) $(INCLUDE_SRCS)
	@mkdir -p bin
	@$(CC) -o bin/$@ -I$(INCLUDE_PATH) $(C_FLAGS) $(C_SRCS)

cpplint:
	@cpplint --quiet --linelength=120 $(C_SRCS) $(HEADERS)

.PHONY: move_gen
