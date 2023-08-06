
#include <immintrin.h>
#include <stdint.h> 

int64_t imsum( uint16_t im[], int n ){
 __m256i s, c;
 __m128i t;
 int i, ni;
 int64_t sum;
 s = _mm256_setzero_si256();
  
 ni = 4;
 for( i = 0; i < n; i = i+4){
     /* read 128 bytes, might not be aligned 
      */
     t = _mm_cvtepu16_epi32( _mm_loadu_si128( (__m128i*) &im[i] ) );
     c = _mm256_cvtepi32_epi64 ( t );
     s = _mm256_add_epi64( s, c );
 }
 sum = _mm256_extract_epi64 (s, 0) + \
       _mm256_extract_epi64 (s, 1) + \
       _mm256_extract_epi64 (s, 2) + \
       _mm256_extract_epi64 (s, 3); 
 return sum;
}