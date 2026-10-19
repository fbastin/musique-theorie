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
  \new StaffGroup <<
    \new Staff \with { instrumentName = \markup \small \italic "régulier" } {
      \clef treble \omit Staff.TimeSignature \cadenzaOn \autoBeamOff \tupletUp
      \textMark \markup \small \italic "duolet" a'8[ a'8 a'8] \bar "|" \textMark \markup \small \italic "quartolet" a'8[ a'8 a'8] \bar "|" \textMark \markup \small \italic "quintolet" a'16[ a'16 a'16 a'16] \bar "|" \textMark \markup \small \italic "septolet" a'16[ a'16 a'16 a'16]
      \bar "|."
    }
    \new Staff \with { instrumentName = \markup \small \italic "irrégulier" } {
      \clef treble \omit Staff.TimeSignature \cadenzaOn \autoBeamOff \tupletUp
      \tuplet 2/3 { a'8[ a'8] } \bar "|" \tuplet 4/3 { a'8[ a'8 a'8 a'8] } \bar "|" \tuplet 5/4 { a'16[ a'16 a'16 a'16 a'16] } \bar "|" \tuplet 7/4 { a'16[ a'16 a'16 a'16 a'16 a'16 a'16] }
      \bar "|."
    }
  >>
  \layout {
    indent = 18\mm line-width = 300\mm
    \context { \Score \override SpacingSpanner.spacing-increment = #1.4 \markLengthOn \override TextMark.self-alignment-X = #LEFT }
  }
}
