#pragma once

#include <stdbool.h>
#include <stdint.h>

class KnowlesMemsDsp {
public:
    static KnowlesMemsDsp& instance();

    bool init();
    void process_audio();

    uint8_t get_latest_dba() const;
    uint32_t get_raw_rms() const;

private:
    KnowlesMemsDsp();

    // Digital Biquad A-Weighting Filter State
    float m_w1, m_w2;
    uint8_t m_latest_dba;
    uint32_t m_raw_rms;
};
