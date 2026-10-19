\version "2.24.3"
%% Fichier produit par outils/generer_valeurs.py — ne pas modifier à la main.
\paper {
  indent = 0
  ragged-right = ##t
  top-margin = 1\mm
  bottom-margin = 1\mm
  left-margin = 1\mm
  right-margin = 1\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
\score {
  \new Staff  {
      \clef treble \omit Staff.TimeSignature \cadenzaOn \autoBeamOff \tupletUp \textLengthOn \override TextScript.staff-padding = #2.5
      r1_\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { "pause" } \bar "|" r2_\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { "demi-pause" } \bar "|" r4_\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { "soupir" } \bar "|" r8_\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { "demi-soupir" } \bar "|" r16_\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { "quart de" "soupir" } \bar "|" r32_\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { "huitième de" "soupir" } \bar "|" r64_\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { "seizième de" "soupir" }
      \bar "|."
    }
  \layout {
     line-width = 300\mm
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \markLengthOn \override TextMark.self-alignment-X = #LEFT }
  }
}
