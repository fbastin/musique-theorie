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
      a'1_\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { "ronde" } \bar "|" a'2_\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { "blanche" } \bar "|" a'4_\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { "noire" } \bar "|" a'8_\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { "croche" } \bar "|" a'16_\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { "double" "croche" } \bar "|" a'32_\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { "triple" "croche" } \bar "|" a'64_\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { "quadruple" "croche" }
      \bar "|."
    }
  \layout {
     line-width = 300\mm
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \markLengthOn \override TextMark.self-alignment-X = #LEFT }
  }
}
