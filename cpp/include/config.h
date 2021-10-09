/***********************************************************************************
 * MIT License
 *
 * Copyright (c) [2021] [Siddhartha (sidmontu@gmail.com)]
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
************************************************************************************/


#pragma once

#include <stdio.h>
#include <stdint.h>
#include <vector>

typedef uint64_t bitboard_t;

typedef struct BoardState {
    bitboard_t black_king;
    std::vector<bitboard_t> black_queens;
    std::vector<bitboard_t> black_rooks;
    std::vector<bitboard_t> black_bishops;
    std::vector<bitboard_t> black_knights;
    std::vector<bitboard_t> black_pawns;
    bitboard_t white_king;
    std::vector<bitboard_t> white_queens;
    std::vector<bitboard_t> white_rooks;
    std::vector<bitboard_t> white_bishops;
    std::vector<bitboard_t> white_knights;
    std::vector<bitboard_t> white_pawns;
} BoardState;
